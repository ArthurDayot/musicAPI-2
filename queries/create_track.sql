-- :name create_track :insert
INSERT INTO tracks(title, album, artist, duration,url,arturl)
VALUES(:title, :album, :artist, :duration, :url, :arturl)
