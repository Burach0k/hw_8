create table Genre(
	genre_id SERIAL PRIMARY KEY,
	name varchar(100) not null
);

create table Performers(
	performer_id SERIAL PRIMARY KEY,
	name varchar(100) not null
);

create table albums(
	album_id SERIAL PRIMARY KEY,
	name varchar(100) not null,
	create_date date check (create_date > '01.01.1800':: Date)
);

create table tracks(
	track_id SERIAL PRIMARY KEY,
	album_id SERIAL references albums(album_id),
	name varchar(100) not null,
	length integer check (length >= 1000)
);
 

create table Compilation(
	compilation_id SERIAL PRIMARY KEY,
	name varchar(100) not null,
	create_date date check (create_date > '01.01.2017':: Date)
);


create table Genre_performer(
	genre_id SERIAL references Genre(genre_id),
	performer_id SERIAL references Performers(performer_id),
	PRIMARY key (genre_id, performer_id)
);

create table Album_performer(
	album_id SERIAL references albums(album_id),
	performer_id SERIAL references Performers(performer_id),
	PRIMARY key (album_id, performer_id)
);


create table compilation_track(
	compilation_id SERIAL references Compilation(compilation_id),
	track_id SERIAL references tracks(track_id),
	PRIMARY key (compilation_id, track_id)
);
