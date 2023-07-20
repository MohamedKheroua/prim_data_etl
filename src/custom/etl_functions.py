"""
    Custom functions defined for :

        - extracting data from the PRIM API 'Prochains Passages de source Ile-de-France Mobilités - Requête globale'
        
        - transforming data

        - and loading it into a PostgreSQL database

"""

import os
import time

import requests

import pandas as pd
from pandas import json_normalize

import json

import psycopg2
from configparser import ConfigParser

from custom import json_dict, replace_in_df_column, concat_values
from custom.chromedriver import chrome
from custom.postgresql import tables

## Extracting data function
def extract_data_from_prim_api(line_ref: str):
    start_of_process_time = time.strftime("%Y%m%d_%H%M%S")
    print("start data extraction at ", start_of_process_time)

    # URLs for connection and loading the csv file
    url_connection = "https://data.iledefrance-mobilites.fr/oidc/login/"

    # Create the Webdriver instance
    mywebdriver = chrome.Chrome()

    # login
    mywebdriver._connect(url_connection=url_connection)

    line_ref = 'ALL'

    # API URL
    api_url = 'https://prim.iledefrance-mobilites.fr/marketplace/estimated-timetable?LineRef=STIF%3ALine%3A%3A'+line_ref+'%3A'


    # The header must contain the API key
    headers = {'Accept': 'application/json','apikey': mywebdriver.my_api_jeton}

    # Request sent
    req = requests.get(api_url, headers=headers)
    print('Status:', req)
    
    return req

## Data transformation function
def transform_prim_data(req_response):
    my_dict = json_dict.only_dict(req_response.content)
    df = json_normalize(my_dict).explode('Siri.ServiceDelivery.EstimatedTimetableDelivery').reset_index(drop=True)

    A = json_normalize(df["Siri.ServiceDelivery.EstimatedTimetableDelivery"].apply(lambda x: json_dict.only_dict(json.dumps(x))).tolist())
    # Join with flattened JSON from key "StopMonitoringDelivery"
    df2 = df[["Siri.ServiceDelivery.ResponseTimestamp",
            "Siri.ServiceDelivery.ProducerRef",
            "Siri.ServiceDelivery.ResponseMessageIdentifier"]].join(A)

    df2 = df2.explode('EstimatedJourneyVersionFrame').reset_index(drop=True)

    B = json_normalize(df2["EstimatedJourneyVersionFrame"].apply(lambda x: json_dict.only_dict(json.dumps(x))).tolist())
    # Join with flattened JSON from key "MonitoredStopVisit"
    df3 = df2.iloc[:,:-1].join(B)

    df3 = df3.explode('EstimatedVehicleJourney').reset_index(drop=True)

    C = json_normalize(df3["EstimatedVehicleJourney"].apply(lambda x: json_dict.only_dict(json.dumps(x))).tolist())
    df4 = df3.iloc[:,:-1].join(C)

    # Timestamp values modified
    replace_in_df_column(df4,["Siri.ServiceDelivery.ResponseTimestamp",
                                "ResponseTimestamp",
                                "RecordedAtTime"], "T", " ")

    replace_in_df_column(df4,["Siri.ServiceDelivery.ResponseTimestamp",
                                "ResponseTimestamp",
                                "RecordedAtTime"], "Z", "")

    # Keeping values from original dictionary if multiples {key, values} exist
    df4["VehicleMode"] = df4["VehicleMode"].apply(lambda x: x[0] if len(x)>0 else "")
    df4["PublishedLineName"] = df4["PublishedLineName"].apply(lambda x: concat_values(x) if len(x)>0 else "")
    df4["DirectionName"] = df4["DirectionName"].apply(lambda x: concat_values(x) if len(x)>0 else "")
    df4["OriginName"] = df4["OriginName"].apply(lambda x: concat_values(x) if len(x)>0 else "")
    df4["DestinationName"] = df4["DestinationName"].apply(lambda x: concat_values(x) if len(x)>0 else "")
    df4["JourneyNote"] = df4["JourneyNote"].apply(lambda x: concat_values(x) if len(x)>0 else "")
    df4["VehicleJourneyName"] = df4["VehicleJourneyName"].apply(lambda x: concat_values(x) if len(x)>0 else "")

    # Null values handling
    df4["DirectionRef.value"] = df4["DirectionRef.value"].fillna(value="")
    df4["OperatorRef.value"] = df4["OperatorRef.value"].fillna(value="")
    df4["RouteRef.value"] = df4["DirectionRef.value"].fillna(value="")
    df4["OriginRef.value"] = df4["DirectionRef.value"].fillna(value="")

    df5 = df4.copy()
    df5 = df5.explode('EstimatedCalls.EstimatedCall').reset_index(drop=True)

    D = json_normalize(df5["EstimatedCalls.EstimatedCall"].apply(lambda x: json_dict.only_dict(json.dumps(x))).tolist())
    cols = [col for col in df5.columns if col!='EstimatedCalls.EstimatedCall']+['EstimatedCalls.EstimatedCall']
    df5=df5[cols]

    # Join with flattened JSON
    df6 = df5.iloc[:,:-1].join(D)

    # Null values handling
    df6["DepartureStatus"] = df6["DepartureStatus"].fillna(value="")
    df6["ArrivalStatus"] = df6["ArrivalStatus"].fillna(value="NO_STATUS")
    df6["ArrivalProximityText.value"] = df6["ArrivalProximityText.value"].fillna(value="")
    df6["ArrivalPlatformName.value"] = df6["ArrivalPlatformName.value"].fillna(value="")

    df6["DestinationDisplay"] = df6["DestinationDisplay"].fillna("").apply(list)
    df6["DestinationDisplay"] = df6["DestinationDisplay"].apply(lambda x: concat_values(x) if len(x)>0 else "")

    # Timestamp values modified
    replace_in_df_column(df6,["ExpectedDepartureTime",
                            "ExpectedArrivalTime",
                            "AimedArrivalTime",
                            "AimedDepartureTime"], "T", " ")

    replace_in_df_column(df6,["ExpectedDepartureTime",
                            "ExpectedArrivalTime",
                            "AimedArrivalTime",
                            "AimedDepartureTime"], "Z", "")

    # Renaming and dropping columns 
    df6.columns = df6.columns.str.replace(".value", "", regex=False)
    df6.drop(columns=["Siri.ServiceDelivery.ResponseTimestamp","Siri.ServiceDelivery.ProducerRef"], inplace=True)  # columns not used

    df6.rename(columns={'Siri.ServiceDelivery.ResponseMessageIdentifier':'ResponseMessageIdentifier'}, inplace=True)

    # Results filtered on a specific transportation line, for example 'C01843'
    # not mandatory ; used here to limit data storage
    # 'C01843' corresponds to the tramway line T4
    line_ref_filtered = 'C01843'

    df_t4 = df6[df6["LineRef"]=="STIF:Line::" + line_ref_filtered + ":"].copy()
    # Condition to test if data is present
    if len(df_t4.index) > 0:
        df_t4 = df_t4.sort_values('RecordedAtTime').drop_duplicates(subset=['DatedVehicleJourneyRef','StopPointRef'],keep='last')
        df_t4 = df_t4.sort_values(by='ExpectedDepartureTime', ascending=True)

        # Specific encoding option for these two columns using special characters (letters with accents)
        df_t4["DestinationName"] = df_t4["DestinationName"].apply(lambda x: x.encode(encoding='ISO-8859-1').decode('latin-1', 'strict'))
        df_t4["DestinationDisplay"] = df_t4["DestinationDisplay"].apply(lambda x: x.encode(encoding='ISO-8859-1').decode('latin-1', 'strict'))

        # Creating new columns which will be used as primary keys for the time and date dimension tables
        columns = ["ExpectedDepartureTime", "ExpectedArrivalTime", "AimedDepartureTime", "AimedArrivalTime"]
        for col in columns:
            name = "id_" + col + "_time"

            tmp = df_t4[col].apply(lambda x: pd.to_datetime(x)).\
                dt.time.\
                fillna(value="").\
                apply(lambda x: int(str(x).replace(":","")) if x else None)
            
            df_t4.insert(df_t4.columns.get_loc(col)+1, name, tmp)
            df_t4[name] = df_t4[name].astype('Int64')
            
            name = "id_" + col + "_date" 
            tmp = df_t4[col].apply(lambda x: pd.to_datetime(x)).\
                dt.date.\
                fillna(value="").\
                apply(lambda x: int(str(x).replace("-","")) if x else None)
            
            df_t4.insert(df_t4.columns.get_loc(col)+1, name, tmp)
            df_t4.drop(columns=col, inplace=True)
            df_t4[name] = df_t4[name].astype('Int64')

        # Reordering the columns, to avoid issues when loading csv files into Postgres tables
        df_t4 = df_t4[["ResponseMessageIdentifier", "ResponseTimestamp", "Version", "Status","RecordedAtTime", "VehicleMode",
                    "PublishedLineName", "DirectionName", "OriginName", "DestinationName",
                    "JourneyNote", "FirstOrLastJourney", "VehicleJourneyName", "LineRef",
                    "DatedVehicleJourneyRef", "DestinationRef", "OperatorRef", "DirectionRef",
                    "RouteRef","OriginRef", "id_ExpectedDepartureTime_date", "id_ExpectedDepartureTime_time",
                    "DestinationDisplay", "DepartureStatus", "id_ExpectedArrivalTime_date",
                    "id_ExpectedArrivalTime_time", "id_AimedArrivalTime_date", "id_AimedArrivalTime_time",
                    "ArrivalStatus", "id_AimedDepartureTime_date", "id_AimedDepartureTime_time",
                    "StopPointRef", "ArrivalPlatformName", "ArrivalProximityText"]]

        end_of_process_time = time.strftime("%Y%m%d_%H%M%S")

        # Saving to a csv file
        df_t4.to_csv('./data/LineRef_STIF_Line_' + line_ref_filtered + '_Date_' + end_of_process_time +'.csv', sep=";", encoding='ISO-8859-1', index=False)

        print("end of data processing at ", end_of_process_time)

    else:
        end_of_process_time = time.strftime("%Y%m%d_%H%M%S")
        print("end of data processing at ", end_of_process_time, " ; no data available for the line ", line_ref_filtered)

## Data loading function to insert data from multiple csv files into Postgres
def load_t4_tram_data(table_to_feed: str, tmp_table: str, schema_tmp_table: str):
    ## Inserting results into PostgreSQL tables
    # read config file
    parser = ConfigParser()
    filename = "src/custom/postgresql/database.ini"
    parser.read(filename)
    conn_params = {}
    section = "postgresql"
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            if os.environ.get(param[1])==None:
                conn_params[param[0]] = param[1].split('"')[1]
            else:
                conn_params[param[0]] = os.environ.get(param[1])
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))


    # connection to PostgreSQL
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**conn_params)
        #Setting auto commit false
        conn.autocommit = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    # List of the csv files to process
    mypath = os.getcwd() + "/data/"

    # List of csv files to process
    files = [f for f in os.listdir(mypath) if f.endswith('.csv')]

    for myfile in files:
        #file path for PostgreSQL access
        file_path = mypath + myfile

        # temporary table used to load csv file
        tables.create_table(conn, tmp_table, schema_tmp_table)

        # load data into temp table
        delimiter=';'
        tables.insert_values_from_csv(conn, tmp_table, file_path, delimiter, encoding='ISO-8859-1')

        # delete row if the primary key is present in the csv file
        # most recent data will replace the oldest data
        # so csv files must be sorted from oldest to latest
        myquery="""
            AS t
            USING  {}
            WHERE  t.DatedVehicleJourneyRef = tmp_table.DatedVehicleJourneyRef
                    AND t.StopPointRef = tmp_table.StopPointRef
            -- AND    t <> d            -- optional, to avoid empty updates
                                        -- only works for complete rows
            ;
            """.format(tmp_table)
        tables.delete_from_table(conn, table_to_feed, myquery)

        # insert data into the target table
        conflit_PK = "DatedVehicleJourneyRef,StopPointRef"
        command = """
            INSERT INTO {}
            TABLE {}    -- short for: SELECT * FROM
            ON CONFLICT ({}) DO NOTHING
            ;
            """.format(table_to_feed, tmp_table, conflit_PK)
        try:
            # create a cursor
            cur = conn.cursor()
            cur.execute(f'{command}')
            print("Data inserted in {} ... ".format(table_to_feed))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        # drop temp table
        tables.drop_table(conn, tmp_table)

        # move processed file into /archive folder
        os.rename(mypath+myfile, mypath+'/archive/'+myfile)

    # Close connexion to the PostgreSQL database server
    try:
        if conn is not None:
            conn.close()
            print('Database connection closed...')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)