"""
    Job for loading data into the Postgres table prochains_passages_T4
    All the csv files in the /data folder will be processed

"""

from src.custom.etl_functions import load_t4_tram_data

schema="""
	ResponseMessageIdentifier VARCHAR(100),
	ResponseTimestamp TIMESTAMP,
	Version NUMERIC,
	Status VARCHAR(20),
	RecordedAtTime TIMESTAMP,
	VehicleMode TEXT,
    PublishedLineName TEXT,
	DirectionName TEXT,
	OriginName TEXT,
	DestinationName TEXT,
	JourneyNote TEXT,
	FirstOrLastJourney TEXT,
	VehicleJourneyName TEXT,
	LineRef TEXT,
	DatedVehicleJourneyRef TEXT,
	DestinationRef TEXT,
	OperatorRef TEXT,
	DirectionRef TEXT,
	RouteRef TEXT,
	OriginRef TEXT,
	id_ExpectedDepartureTime_date INT,
	id_ExpectedDepartureTime_time INT,
	DestinationDisplay TEXT,
	DepartureStatus TEXT,
	id_ExpectedArrivalTime_date INT,
	id_ExpectedArrivalTime_time INT,
	id_AimedArrivalTime_date INT,
	id_AimedArrivalTime_time INT,
	ArrivalStatus TEXT,
	id_AimedDepartureTime_date INT,
	id_AimedDepartureTime_time INT,
	StopPointRef TEXT,
	ArrivalPlatformName TEXT,
	ArrivalProximityText TEXT,
    PRIMARY KEY (DatedVehicleJourneyRef,StopPointRef)
    """

table_T4 = "prochains_passages_T4"
tmp_table = "tmp_table"

# Load data
load_t4_tram_data(table_to_feed = table_T4, tmp_table = tmp_table, schema_tmp_table = schema)