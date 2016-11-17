import os
import sqlite3
from flask import  g
	
from hedgehog import app

def connect_db():
	""" Connect to db """
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv
	
def get_db():
	"""oppens a new db connection if it is not already openned"""
	if not hasattr(g,'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	"""Closes the db at the end of request"""
	if hasattr(g,'sqlite_db'):
		g.sqlite_db.close()
		
############################
#		Init DB			   #
############################
def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()
	
@app.cli.command('initdb')
def initdb_command():
	"""Initializes db."""
	init_db()
	print("Initialized databases.")
###############################	
