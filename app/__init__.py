from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from coreapi import CoreAPI

#from flaskext.mysql import MySQL

app = Flask(__name__)
app.config.from_object('config')

CoreAPI.check_app(app)
coreapi = CoreAPI(app)

db = SQLAlchemy(app)

from app import controllers, models
