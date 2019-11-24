-- $ sqlite3 music.db < sqlite.sql

BEGIN TRANSACTION;

DROP TABLE IF EXISTS playlist;
CREATE TABLE playlist (
    id INTEGER PRIMARY KEY,
    userid INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR NULL,
    UNIQUE(userid,title)
);

DROP TABLE IF EXISTS playlist_tracks;
CREATE TABLE playlist_tracks(
    playlist_id INTEGER NOT NULL,
    track_id INTEGER NOT NULL,
);


DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    firstname VARCHAR NOT NULL,
    lastname VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    UNIQUE(username)
);

DROP TABLE IF EXISTS descriptions;
CREATE TABLE descriptions (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	description VARCHAR NOT NULL,
	username VARCHAR NOT NULL,
	url VARCHAR NOT NULL
);
