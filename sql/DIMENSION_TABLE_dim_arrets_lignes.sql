-- Create dim_arrets_lignes
CREATE TABLE dim_arrets_lignes
(
	route_id VARCHAR(20),
    route_long_name TEXT,
    stop_id VARCHAR(50),
    stop_name VARCHAR(100),
    stop_lon NUMERIC,
    stop_lat NUMERIC,
    OperatorName VARCHAR(100),
    Pointgeo VARCHAR(50),
    Nom_commune VARCHAR(100),
    Code_insee INTEGER,
    PRIMARY KEY (route_id, stop_id)
);

-- Copy static data from csv file
-- original file available here : https://prim.iledefrance-mobilites.fr/fr/donnees-statiques/arrets-lignes
COPY dim_arrets_lignes
FROM 'arrets-lignes.csv'
DELIMITER ';'
ENCODING 'UTF8'
CSV HEADER;