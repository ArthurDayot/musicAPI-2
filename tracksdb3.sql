DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks (
    uuid INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    album VARCHAR NOT NULL,
    artist VARCHAR NOT NULL,
    duration VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    artUrl VARCHAR NULL,
    UNIQUE(title, artist)
);
