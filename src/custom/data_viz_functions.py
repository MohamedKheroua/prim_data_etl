import os

from configparser import ConfigParser

from sqlalchemy import create_engine

import pandas as pd
import sqlalchemy as sa

import plotly.express as px

# Bar chart data visualisation of the data from the table 'prochains_passages_T4'
def bar_chart_data_viz(day_of_month: int, month: int, year: int, destination: str, html_file: str):
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
    engine = create_engine('postgresql://' + conn_params["user"] +
                        ':' + conn_params["password"] +
                        '@' + conn_params["host"] +
                        ':5432/' + conn_params["dbname"])

    # Table used for selecting data to visualise
    mytable = "prochains_passages_T4"

    # SQL command to create the aggregated data
    # Percentage of tramways heading to the station {destination}, filtered on {day_of_month, month, year}, given by status and by station
    command = """
    SELECT
        arrets.arrname as "Arrêt",
        t4.destinationname as "Destination",
        date.year_actual as "Année",
        date.month_name as "Mois",
        date.day_of_month as "Jour",
        t4.arrivalstatus as "Statut",
        ROUND(AVG(time1.second_of_day - time2.second_of_day), 2) AS "Retard moyen (s)",
        count(t4.datedvehiclejourneyref) as "Nb trains",
        ROUND(COUNT(*)*100 / (SUM(count(*)) over (partition by arrets.arrname, t4.destinationname)), 2) as "% statut"
    FROM {} as t4
    LEFT JOIN public.dim_arrets as arrets
        ON t4.lineref = arrets.lineref
        AND t4.stoppointref = arrets.monitoringref_arr
    LEFT JOIN public.dim_date as date
        ON t4.id_aimedarrivaltime_date = date.date_dim_id
    LEFT JOIN public.dim_time as time1
        ON t4.id_expectedarrivaltime_time = time1.id
    LEFT JOIN public.dim_time as time2
        ON t4.id_aimedarrivaltime_time = time2.id
    WHERE t4.arrivalstatus <> 'NO_STATUS'
        AND date.day_of_month = {}
        AND date.month_actual = {}
        AND date.year_actual = '{}'
        AND t4.destinationname = '{}'
        AND arrets.arrname in ('Aulnay-sous-Bois', 'Rougemont Chanteloup', 'Freinville Sevran', 'L''Abbaye', 'Lycée Henri Sellier', 'Gargan', 'Les Pavillons-sous-Bois T4', 'Allée de la Tour Rendez Vous', 'Les Coquetiers', 'Remise à Jorelle', 'Bondy')
    GROUP BY
        arrets.arrname,
        t4.destinationname,
        date.year_actual,
        date.month_name,
        date.day_of_month,
        t4.arrivalstatus
    ORDER BY
        CASE arrets.arrname
            when 'Aulnay-sous-Bois' then 0 
            when 'Rougemont Chanteloup' then 1
            when 'Freinville Sevran' then 2
            when 'L''Abbaye' then 3
            when 'Lycée Henri Sellier' then 4
            when 'Gargan' then 5
            when 'Les Pavillons-sous-Bois T4' then 6
            when 'Allée de la Tour Rendez Vous' then 7
            when 'Les Coquetiers' then 8
            when 'Remise à Jorelle' then 9
            when 'Bondy' then 10
            end,
        t4.destinationname,
        date.year_actual,
        date.month_name,
        date.day_of_month,
        t4.arrivalstatus ASC;
    """.format(mytable, day_of_month, month, year, destination)

    # Use of the pandas method 'read_sql_query' to create a DataFrame from the SQL query
    with engine.begin() as conn:
        data = pd.read_sql_query(sa.text(command), conn)

    # Bar graph visualisation
    fig = px.bar(data,
                x="Arrêt",
                y="% statut",
                color="Statut",
                text="% statut",
                orientation="v",
                width=850, height=1000)
    fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)

    fig.update_layout(
    title={
        'text': """<b><span style="font-size: 15pt">Proportion de tramways répartis par station et par statut</span></b>
                    <br><i>Tramway T4 - direction {} - {}/{}/{}</i>
                    """.format(destination, day_of_month, month, year),
        'x': 0,
        'y': 0.9,
        'xref': 'paper',
        'yref': 'container',
        'xanchor': 'left',
        'yanchor': 'middle'},
    xaxis_title="<b>arrêts</b>",
    legend_title="statut",
    font=dict(
        family="Arial",
        size=12
    ),
        template=None
    )
    fig.update_xaxes(tickangle=-45)

    # Y title removed, replaced with an annotation
    # Original Y title cannot be rotated
    fig.update_layout(yaxis_title=None)
    fig.add_annotation(
        align="center",
        font=dict(
        family="Arial",
        size=14
        ),
        xref="x domain",
        yref="y domain",
        x=-0.20,
        y=0.5,
        text="<br><b>%</b><br><b>trains</b>",
        showarrow=False
    )

    fig.update_layout(margin=dict(l=150, r=150, t=200, b=200),paper_bgcolor = "pink")

    # Data visualisation saved in html format to keep its interactivity
    fig.write_html('data/' + html_file)