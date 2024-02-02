DROP DATABASE IF EXISTS seattle_crime_db;
CREATE DATABASE seattle_crime_db;

CREATE OR REPLACE TABLE offenses (
  id SERIAL PRIMARY KEY NOT NULL,
  report_id INTEGER,
  offense_detail_id INTEGER,
  offense_start_datetime TIMESTAMP,
  offense_end_datetime TIMESTAMP

);


