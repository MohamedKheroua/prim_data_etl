-- Create dim_perimetre_des_donnees_tr_disponibles_plateforme_idfm
CREATE TABLE dim_perimetre_des_donnees_tr_disponibles_plateforme_idfm
(
	MonitoringRef_ArR TEXT NOT NULL,
	ArRName TEXT,
	LineRef TEXT,
	Name_Line TEXT,
	PRIMARY KEY (MonitoringRef_ArR, LineRef)
);

-- Copy static data from csv file
-- original file available here : https://prim.iledefrance-mobilites.fr/fr/donnees-statiques/perimetre-des-donnees-tr-disponibles-plateforme-idfm
COPY dim_perimetre_des_donnees_tr_disponibles_plateforme_idfm
FROM 'perimetre-des-donnees-tr-disponibles-plateforme-idfm.csv'
DELIMITER ';'
ENCODING 'UTF8'
CSV HEADER;


-- Create derivated view
CREATE VIEW dim_dv_perimetre_des_donnees_tr_disponibles_plateforme_idfm AS
select
	MonitoringRef_ArR,
	concat('IDFM:',split_part(MonitoringRef_ArR, ':', 4)) as stop_id,
	ArRName,
	LineRef,
	concat('IDFM:',split_part(LineRef, ':', 4)) as route_id,
	Name_Line
from public.dim_perimetre_des_donnees_tr_disponibles_plateforme_idfm;


-- Create dimension table dim_arrets
create view dim_arrets as 
select
	a.MonitoringRef_ArR,
	a.stop_id,
	b.stop_name,
	b.stop_lon,
	b.stop_lat,
	b.pointgeo,
	a.ArRName,
	a.LineRef,
	a.route_id,
	b.route_long_name,
	a.Name_Line,
	b.operatorname,
	b.nom_commune,
	b.code_insee
from public.dim_dv_perimetre_des_donnees_tr_disponibles_plateforme_idfm as a
LEFT JOIN public.dim_arrets_lignes as b
	ON a.stop_id = b.stop_id
	and a.route_id = b.route_id;