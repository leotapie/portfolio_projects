
create table date_dim (
	date_key integer PRIMARY KEY,
	full_date date,
	month integer,
	day integer,
	month_name varchar(20),
	day_name varchar(20),
	weekend boolean
);


create table stations (
	id integer PRIMARY KEY,
	station_name varchar(50),
	latitude real,
	longitude real
);

create table trip_demo (
	id integer PRIMARY KEY,
	user_type varchar(50),
	gender integer,
	birth_year integer,
	age integer
);


create table weather (
	id serial PRIMARY KEY,
	rec_date date,
	avg_wind real,
	prcp real,
	snowfall real,
	snow_depth real,
	t_avg integer,
	t_max integer,
	t_min integer,
	date_key integer,
	rain boolean,
	snow boolean,
	FOREIGN KEY(date_key) REFERENCES date_dim(date_key)
);


create table rides (
	id integer PRIMARY KEY,
	date_key integer,
	trip_duration integer,
	trip_duration_min real,
	trip_duration_hrs real,
	start_time timestamp,
	stop_time timestamp,
	start_station_id integer,
	end_station_id integer,
	bike_id integer,
	valid_duration boolean,
	trip_demo integer,
	FOREIGN KEY(date_key) REFERENCES date_dim(date_key),
	FOREIGN KEY(start_station_id) REFERENCES stations(id),
	FOREIGN KEY(end_station_id) REFERENCES stations(id),
	FOREIGN KEY(trip_demo) REFERENCES trip_demo(id)
);