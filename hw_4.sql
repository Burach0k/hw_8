--drop table genre cascade;
--drop table Performers cascade;
--drop table albums cascade;
--drop table tracks cascade;
--drop table Compilation cascade;
--drop table Genre_performer;
--drop table Album_performer;
--drop table compilation_track;

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

insert into Performers (name)
values ('Andrei'), ('Ivan'), ('Tanya'), ('Alex'), ('Jon'), ('Tom'), ('Katya'), ('EvGENI'), ('mr andersen')

insert into genre (name)
values ('jaz'), ('bluz'), ('folk'), ('electrical'), ('shanson')

insert into albums (name, create_date)
values ('Besl album', '10.11.2020'::Date), ('Blr live', '10.11.2019'::Date), ('D&D', '20.05.1993'::Date), ('OOP in music', '01.01.1801'::Date),
('k-p-o', '11.12.1963'::Date), ('Blue Marine', '08.10.2022'::Date), ('Future live', '13.01.2041'::Date), ('I&Y', '01.01.2021'::Date), ('RRR', '01.01.2018'::Date)


insert into tracks (album_id, name, length)
values (1, 'in the end', 5 * 60 * 60), (1, 'in the start', 5 * 60 * 60), (2, 'unnnamed', 4.6 * 60 * 60), (2, 'i love sivyhin', 5.1 * 60 * 60),
(3, 'guns', 4 * 60 * 60), (3, 'banka parilka', 3 * 60 * 60), (4, 'vesenni les', 3.3 * 60 * 60), (5,'3 sentabra', 10 * 60 * 60 * 60),
(5, 'numa numa e', 5 * 60 * 60), (6,'kazanova', 4.6 * 60 * 60), (6,'tam gde zreet vinograd', 3.6 * 60 * 60), (7,'nas ne dogonyat', 5 * 60 * 60),
(8, 'znaesh li ti', 5.01 * 60 * 60), (9, 'kytystrica', 5.5 * 60 * 60), (9, 'my gun', 5.3 * 60 * 60), (3, 'in the end_2', 5 * 60 * 60), (3, 'in the start_2', 5 * 60 * 60)

insert into compilation (name, create_date)
values ('my', now()), ('for work', '13.12.2022'::Date), ('for sport', '13.12.2022'::Date), ('for game', '01.12.2017'::Date), ('for dancing', '03.03.2033'::Date)
, ('for bad work', '13.12.2022'::Date), ('for relax', '13.01.2019'::Date), ('for vanna', '02.06.2018'::Date)


insert into genre_performer (performer_id, genre_id) values (1,1), (2,2), (3,3), (3,1), (3,5), (4,4), (5,5), (5,3), (5,1), (6,2), (7,2), (8, 3), (8, 1), (8, 5)


insert into album_performer (performer_id, album_id) values (1,1), (2,2), (3,3), (3,1), (3,6), (4,4), (5,5), (5,7), (5,8), (6,2), (7,2), (8, 3), (8, 8), (8, 5)


insert into compilation_track (track_id, compilation_id) values (1, 1), (2, 2), (3, 3), (4, 3), (5,4), (6,4), (7,5), (8,7), (9,6), (10, 6), (11, 8), (12, 3), (13, 4), (14, 5), (15, 8)

-------------------------------------------------------

-- количество исполнителей в каждом жанре;
select gp_count.count as "количество исполнителей", g.name from genre g
join (select count(gp.performer_id), gp.genre_id from genre_performer gp
	  group by gp.genre_id) gp_count on gp_count.genre_id = g.genre_id 

-- количество треков, вошедших в альбомы 2019-2020 годов;
select count(*) as "количество треков за 2019-2020" from albums a where extract(year from create_date) between '2019' and '2020'

-- средняя продолжительность треков по каждому альбому;
select name, avg as "средняя продолжительность треков" from albums a
join (select avg(t.length), t.album_id from tracks t
	  group by t.album_id) t_avg on t_avg.album_id = a.album_id

-- все исполнители, которые не выпустили альбомы в 2020 году;
select pf.name as "исполнители" from performers pf
join (select distinct ap.performer_id from albums a
	  join album_performer ap on ap.album_id = a.album_id
	  where extract(year from a.create_date) = '2020') ap_2020 on ap_2020.performer_id = pf.performer_id  

-- названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
select c."name" as "названия сборников" from compilation c 
join compilation_track ct on ct.compilation_id = c.compilation_id
join tracks t on t.track_id = ct.track_id
join album_performer ap on ap.album_id = t.album_id
join performers p on p.performer_id = ap.performer_id
where p."name" = 'Andrei'

-- название альбомов, в которых присутствуют исполнители более 1 жанра;
select a."name" from album_performer ap
join (select gp.performer_id from genre_performer gp
	  group by gp.performer_id
	  having count(gp.genre_id) > 1) pref_with_genre_more_1 on ap.performer_id = pref_with_genre_more_1.performer_id
join albums a on a.album_id = ap.album_id

-- наименование треков, которые не входят в сборники;
select t."name" from tracks t
left join compilation_track ct on t.track_id = ct.track_id
where ct.compilation_id is null 

-- исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
select p."name" from album_performer a
join performers p on p.performer_id = a.performer_id 
join (select * from tracks t
	  where length = (select min(length) from tracks)) min_track_length on min_track_length.album_id = a.album_id

-- название альбомов, содержащих наименьшее количество треков.
select a.name from albums a
join (select t.album_id from tracks t
	  group by t.album_id
	  having count(t.track_id) = (select count(t.track_id) from tracks t group by t.album_id order by count limit 1)
	 ) album_id_with_min_track_count on album_id_with_min_track_count.album_id = a.album_id

