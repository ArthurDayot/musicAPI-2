from flask import Flask, jsonify
#app = Flask(__name__)

import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import pugsql
import uuid
import sqlite3

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')
queries = pugsql.module('queries/')
queries2 = pugsql.module('queries/')
queries3 = pugsql.module('queries/')
queries4 = pugsql.module('queries/')

queries.connect(app.config['DATABASE_URL'])
queries2.connect(app.config['DATABASE_URL2'])
queries3.connect(app.config['DATABASE_URL3'])
queries4.connect(app.config['DATABASE_URL4'])

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('tracksdb1.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        with app.open_resource('tracksdb2.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        with app.open_resource('tracksdb3.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/', methods=['GET'])
def home():
    return '''<h1>SPOTIFY, but without music streaming</h1>
    <h2>TRACKS MICROSERVICE</h2>
<p>A prototype API for delivering track, playlist, and user data.</p>'''

@app.route('/api/resources/tracks/all', methods=['GET'])
def all_tracks():
    all_tracks = queries.all_tracks()
    return list(all_tracks)

#GET track that matches id number
@app.route('/api/resources/tracks/<int:id>', methods=['GET'])
def track(id):
    if id % 3 == 0:
        return queries.track_by_id(id=id)
    elif id % 3 == 1:
        return queries2.track_by_id(id=id)
    elif id % 3 == 2:
        return querie3.track_by_id(id=id)

@app.route('/api/resources/tracks', methods=['GET', 'POST'])
def tracks():
    if request.method == 'GET':
        return filter_tracks(request.args)
    elif request.method == 'POST':
        return create_track(request.data)

@app.route('/api/resources/tracks/update', methods=['GET','PUT'])
def updates():
    if request.method == 'GET':
        return (list(queries.all_tracks()))
    if request.method == 'PUT':
        return update_track(request.data)

@app.route('/api/resources/tracks/delete/<int:id>', methods=['GET','DELETE'])
def deletes(id):
    if request.method =='GET':
        return (list(queries.all_tracks()))
    if request.method == 'DELETE':
        return delete_track(id)

def delete_track(id):
    track_to_delete = id
    filter_query =[]
    try:
        query = "DELETE FROM tracks WHERE uuid=?"
        filter_query.append(track_to_delete)
        queries._engine.execute(query,filter_query)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_404_NO_CONTENT
    return '', status.HTTP_204_NO_CONTENT

#When posting to flask api, erase trailing whitespaces,
#{"title":"Blue Submarine","album":"Yellow Submarine","artist":"The Beatles","duration":"3:20","url":"C://songs/s24","arturl":"C;//song/img/s24"},{"title":"Yellow Submarine","album":"Yellow Submarine","artist":"The Beatles","duration":"3:20","url":"C://songs/s23","arturl":"C;//song/img/s23"}
#{"title":"Yellow Submarine","album":"Yellow Submarine","artist":"The Beatles","duration":"3:20","url":"C://songs/s23","arturl":"C;//song/img/s23"}
def create_track(track):
    track = request.data
    required_fields = ['title', 'album', 'artist', 'duration','url']

    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        id = uuid.uuid4()
        track['id'] = queries.create_track(**track)

        import pprint
        pprint.pprint(track)
        if int(id) % 3 == 0:
                queries2.create_track(**track)
        elif int(id) % 3 == 1:
                queries3.create_track(**track)
        elif int(id) % 3 == 2:
                queries4.create_track(**track)

    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return track, status.HTTP_201_CREATED

#PUT Method - Requires 'id' or 'artist title'
def update_track(track):
    search_by_id = ['columnName','columnValue','id']
    search_by_unique_constraint = ['columnName','columnValue','title', 'artist']
    track = request.data
    to_filter = []

#{"changeColumn":"title","changeValueTo":"Yellow Submarine", "artist": "The Beatles","title":"old song"}
    if 'changeColumn' in track and 'changeValueTo' in track and 'title' in track and 'artist' in track:
        title = track['title']
        artist = track['artist']
        columnName = track['changeColumn']
        columnValue = track['changeValueTo']
        query = "UPDATE tracks SET {}=? WHERE title=? AND artist=?".format(columnName)
        to_filter.append(columnValue)
        to_filter.append(title)
        to_filter.append(artist)
        queries._engine.execute(query,to_filter)
#{"changeColumn":"title","changeValueTo":"Yellow Submarine","uuid":"2"}
    elif 'changeColumn' in track and 'changeValueTo' in track and 'id' in track:
        columnName = track['changeColumn']
        query = "UPDATE tracks SET {}=? WHERE uuid =?".format(columnName)
        to_filter.append(track['changeValueTo'])
        to_filter.append(track['id'])
        queries._engine.execute(query,to_filter)
    return track, status.HTTP_201_CREATED


#Search for track based off given parameter
def filter_tracks(query_parameters):
    id = query_parameters.get('id')
    title = query_parameters.get('title')
    album = query_parameters.get('album')
    artist = query_parameters.get('artist')
    #duration = query_parameters.get('duration')
    #url = query_parameters.get('url')
    #arturl = query_parameters.get('arturl')

    query = "SELECT * FROM tracks WHERE"
    to_filter = []

    if id:
        query += ' uuid=? AND'
        to_filter.append(id)
    if title:
        query += ' title=? AND'
        to_filter.append(title)
    if album:
        query += ' album=? AND'
        to_filter.append(album)
    if not (id or title or album or artist):
        raise exceptions.NotFound()
    query = query[:-4] + ';'

    results = queries._engine.execute(query, to_filter).fetchall()
    #one = results['title']
    #return results
    #return list(results)
    return list(map(dict, results))
