#imports

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import twilio.twiml

#configs
DATABASE = '/tmp/banana.db'
DEBUG = True
SECRET_KEY = 'oscar and bambi'
USERNAME = 'admin'
PASSWORD = '12345'

#creating app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('BANANA_SETTINGS', silent=True)

#database stuff
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#ROUTING
@app.route('/hello')
def hello():
    return 'Hello World!'

@app.route('/text', methods=['GET', 'POST'])
def hello_text():
    resp = twilio.twiml.Response()
    resp.message("Hello, This is the banana phone!")
    return str(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0')



