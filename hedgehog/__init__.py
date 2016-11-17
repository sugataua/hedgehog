# imports
import os
from flask import Flask
from hedgehog import configmodule

app = Flask(__name__)
app.secret_key = '\x9c\xcd\xe4\x1c\xd1b\x01\x1c\xf8\xda\\h\xe1L\x92\xa9@2\xb1'

""" Config part """
app.config.from_object(configmodule.DevelopmentConfig)
app.config.from_envvar('FLASK_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.root_path + "\\" + 'flask_alchemy.db'

from hedgehog import db
from hedgehog import views
from hedgehog import model






