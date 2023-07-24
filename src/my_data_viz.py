"""
    An example of a bar chart visualisation of aggregated data from the table 'prochains_passages_T4'
    Percentage of tramways :
        - heading to the terminal station 'Aulnay-sous-Bois'
        - on the day of July 18th, 2013
        - and given by status and by station
"""

from src.custom.data_viz_functions import bar_chart_data_viz

# Filters used in the WHERE clause of the SQL command
filter_day_of_month = 18
filter_month = 7
filter_year = 2023
filter_destination = 'Aulnay-sous-Bois'

bar_chart_data_viz(day_of_month=18, month=7, year=2023, destination='Aulnay-sous-Bois', html_file="20230718_my_bar_graph.html")