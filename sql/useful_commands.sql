-- Useful SQL commands, to check databases and tables size in disk
-- (source : http://www.thegeekstuff.com/2009/05/15-advanced-postgresql-commands-with-examples/)

SELECT pg_size_pretty(pg_database_size('prim_database'));

SELECT pg_size_pretty(pg_total_relation_size('dim_arrets_lignes'));