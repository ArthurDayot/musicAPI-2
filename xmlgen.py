#from flask import Flask, jsonify
#app = Flask(__name__)

import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import pugsql
import requests
app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')
queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('createdb.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/', methods=['GET'])
def home():
    r = requests.get('http://localhost:5000/playlist/all')
    json = r.json()
    print (json)
    return '''<h1>SPOTIFY, but without music streaming</h1>
    <h2>XML GENERATOR MICROSERVICE</h2>
<p>A prototype API for delivering track, playlist, and user data.</p>'''
	#r = requests.get('http://localhost:5000/playlist/all')
	#json = r.json()
	#print json

#GET all playlist that matches user id number
@app.route('/playlist/select/<int:id>', methods=['GET'])
def playlist_selection(id):
    to_filter = []
    to_filter.append(id)
    query = "SELECT * FROM playlist WHERE userid=?"
    results = queries._engine.execute(query, to_filter).fetchall()
    return list(map(dict, results))

#list all the playlists
@app.route('/playlist/all', methods=['GET'])
def select_all():
    all_playlists = queries.select_all_playlist()
    if all_playlists:
        return list(all_playlists)
    return '<h1>No Playlist in database</h1>'

@app.route('/test',methods=['GET'])
def select_playlist():
	payload = {'id':1}
	r = requests.get('http://localhost:5000/playlist/display', params=payload)
	json = r.json()
	print (json)
	return json

#Playlist title into xml

#Loop through each track_id and use query/microservice to retevie info

#xml that info

