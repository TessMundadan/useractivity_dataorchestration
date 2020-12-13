DROP TABLE public.songs
DROP TABLE public.time
DROP TABLE public.artists
DROP TABLE public.songplays
DROP TABLE public.staging_events
DROP TABLE public.staging_songs
DROP TABLE public.users



CREATE TABLE public.artists (
	artistid varchar(256) NOT NULL,
	name varchar(MAX),
	location varchar(MAX),
	lattitude numeric(18,0),
	longitude numeric(18,0)
);

CREATE TABLE public.songplays (
	playid varchar(32) NOT NULL,
	start_time timestamp NOT NULL,
	userid int4 NOT NULL,
	"level" varchar(MAX),
	songid varchar(256),
	artistid varchar(256),
	sessionid int4,
	location varchar(MAX),
	user_agent varchar(MAX),
	CONSTRAINT songplays_pkey PRIMARY KEY (playid)
);

CREATE TABLE public.songs (
	songid varchar(256) NOT NULL,
	title varchar(MAX),
	artistid varchar(256),
	"year" int4,
	duration numeric(18,0),
	CONSTRAINT songs_pkey PRIMARY KEY (songid)
);

CREATE TABLE public.staging_events (
	artist varchar(MAX),
	auth varchar(MAX),
	firstname varchar(MAX),
	gender varchar(256),
	iteminsession int4,
	lastname varchar(MAX),
	length numeric(18,0),
	"level" varchar(MAX),
	location varchar(MAX),
	"method" varchar(MAX),
	page varchar(MAX),
	registration numeric(18,0),
	sessionid int4,
	song varchar(MAX),
	status int4,
	ts int8,
	useragent varchar(MAX),
	userid int4
);

CREATE TABLE public.staging_songs (
	num_songs int4,
	artist_id varchar(256),
	artist_name varchar(MAX),
	artist_latitude numeric(18,0),
	artist_longitude numeric(18,0),
	artist_location varchar(MAX),
	song_id varchar(256),
	title varchar(MAX),
	duration numeric(18,0),
	"year" int4
);



CREATE TABLE public.users (
	userid int4 NOT NULL,
	first_name varchar(MAX),
	last_name varchar(MAX),
	gender varchar(MAX),
	"level" varchar(MAX),
	CONSTRAINT users_pkey PRIMARY KEY (userid)
);

CREATE TABLE public.time (
    start_time timestamp NOT NULL,
    hour INT, 
    day INT, 
    week INT, 
    month INT, 
    year INT, 
    weekday INT,
    CONSTRAINT time_pkey PRIMARY KEY (start_time)
);   
