# imports
import os
from flask import Flask
from hedgehog import configmodule
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '\x9c\xcd\xe4\x1c\xd1b\x01\x1c\xf8\xda\\h\xe1L\x92\xa9@2\xb1'

db = SQLAlchemy(app)


basedir = os.path.abspath(os.path.dirname(__file__))

login_manager = LoginManager()
login_manager.init_app(app)

""" Config part """
app.config.from_object(configmodule.DevelopmentConfig)
app.config.from_envvar('FLASK_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'flask_alchemy.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + 'test:test@localhost:3306/hedgehog'
app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')

from hedgehog import db
from hedgehog import views
from hedgehog import model

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()






