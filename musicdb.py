#from flask import Flask, jsonify
#app = Flask(__name__)

import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import pugsql

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

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('createdb.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

        with app.app_context():
            db = queries2._engine.raw_connection()
            with app.open_resource('tracksdb1.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

        with app.app_context():
            db = queries3._engine.raw_connection()
            with app.open_resource('tracksdb2.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

        with app.app_context():
            db = queries4._engine.raw_connection()
            with app.open_resource('tracksdb3.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
