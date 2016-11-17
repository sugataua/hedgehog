DROP TABLE IF EXISTS towns;

CREATE TABLE towns (
	id INTEGER PRIMARY KEY autoincrement,
	name TEXT NOT NULL,
	population INTEGER,		
	/*
	Район
	Область	
	*/
);

DROP TABLE IF EXISTS stations;

CREATE TABLE stations (
	id INTEGER PRIMARY KEY,
	name TEXT,
	transport TEXT, /* BUS, RAILWAY */ 
	town_id INTEGER,
	coord_lat REAL,
	coord_lon REAL,
	work_hours_start TEXT,
	work_hours_end TEXT,
	luggage_storage INTEGER,
	toilet INTEGER,
	ticket_office INTEGER,
	waiting_room INTEGER,
	
	FOREIGN KEY(town_id) REFERENCES towns(id)
);


DROP TABLE IF EXISTS photo_schedule;

CREATE TABLE photo_schedule(
	id INTEGER PRIMARY KEY,
	station_id INTEGER,
	town_id INTEGER,
	dt_created DATETIME DEFAULT CURRENT_TIMESTAMP,
	image_link TEXT,
	user_comment TEXT,
	
	FOREIGN KEY(station_id) REFERENCES stations(id),
	FOREIGN KEY(town_id) REFERENCES towns(id)
);
