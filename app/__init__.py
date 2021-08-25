from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_jwt_extended import JWTManager
import redis


app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

db = SQLAlchemy(app)
conn = db.engine.raw_connection()

# rd = redis.StrictRedis(host='localhost', db=5)
rd = redis.StrictRedis(host='lingshipu.ren', db=5)
jwt = JWTManager(app)

from .home import home
from .api import api

app.register_blueprint(api,url_prefix='/api/v1.0') # /api/v1.0/home
app.register_blueprint(home,url_prefix='/')


