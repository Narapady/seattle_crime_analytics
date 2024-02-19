CREATE TABLE reports (
  id SERIAL PRIMARY KEY NOT NULL,
  report_numer VARCHAR(255),
  report_datetime TIMESTAMP
);

CREATE TABLE offense_groups (
  id SERIAL PRIMARY KEY NOT NULL,
  group_a_b VARCHAR(10),
  parent_group VARCHAR(10),
  description VARCHAR(100),
  offense_code VARCHAR(3),
  crime_category VARCHAR(255)
);

CREATE TABLE offense_locations (
  id SERIAL PRIMARY KEY NOT NULL,
  longitude NUMERIC(12,8),
  latitude NUMERIC(12,8)
);

CREATE TABLE designated_police_locations (
  id SERIAL PRIMARY KEY NOT NULL,
  precint VARCHAR(10),
  sector VARCHAR(10),
  mcpp VARCHAR(50),
  address_100_block VARCHAR(255)
);

CREATE TABLE offense_details (
  id SERIAL PRIMARY KEY NOT NULL,
  offense_location_id INTEGER,
  designated_police_location_id INTEGER,
  offense_group_id INTEGER,
  CONSTRAINT fk_offense_location_id FOREIGN KEY (offense_location_id) REFERENCES offense_locations (id) ON DELETE CASCADE,
  CONSTRAINT fk_designated_police_location_id FOREIGN KEY (designated_police_location_id) REFERENCES designated_police_locations (id) ON DELETE CASCADE,
  CONSTRAINT fk_offense_group_id FOREIGN KEY (offense_group_id) REFERENCES offense_groups (id) ON DELETE CASCADE
);

CREATE TABLE offenses (
  id SERIAL PRIMARY KEY NOT NULL,
  report_id INTEGER,
  offense_detail_id INTEGER,
  offense_start_datetime TIMESTAMP,
  offense_end_datetime TIMESTAMP,
  CONSTRAINT fk_report FOREIGN KEY (report_id) REFERENCES reports (id) ON DELETE CASCADE,
  CONSTRAINT fk_offense_detail FOREIGN KEY (offense_detail_id) REFERENCES offense_details (id) ON DELETE CASCADE
);


