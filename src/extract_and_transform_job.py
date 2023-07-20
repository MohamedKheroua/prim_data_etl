"""
    Job for extracting and transforming data from API 'Prochains Passages de source Ile-de-France Mobilités - Requête globale'
    Data for all the available lines (parameter line_ref = 'ALL') are processed

"""

from src.custom.etl_functions import extract_data_from_prim_api, transform_prim_data

# Extract
line_ref = 'ALL'
req_resp = extract_data_from_prim_api(line_ref = line_ref)

# Transform
transform_prim_data(req_resp)