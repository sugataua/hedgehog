# imports

"""
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

#create app
app = Flask(__name__)
app.config.from_object(__name__)

#Load default settings
app.config.update(dict(
	DATABASE=os.path.join(app.root_path,'flask.db'),
	SECRET_KEY='dev key',
	USERNAME='admin',
	PASSWORD='default'
))

app.config.from_envvar('FLASK_SETTINGS', silent=True)


def connect_db():
	# Connect to db 
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv
	
	
"""