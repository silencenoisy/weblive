from . import home
from app.models import Test,Room
from app import db,conn,jwt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,create_refresh_token,
)

from flask import render_template,redirect,url_for,jsonify,Response,request
from random import randrange


@home.route('/',methods=['GET'])
def index():
    return render_template('g.html')

@home.route('/live/<room>',methods=['GET'])
def live_room(room):
    return render_template('play_room.html')


@home.route('/login',methods=['GET','POST'])
def login_index():
    return render_template('login.html')


@home.route('/user/<account>',methods=['GET'])
def user_index(account):
    return render_template("user_index.html")

@home.route('/g',methods=['GET'])
def type_sort():
    return render_template("g.html")


@home.route('/g/<type_name>',methods=['GET'])
def type_liver(type_name):
    return render_template("type_liver.html")


@home.route('/liver',methods=['GET'])
def liver_index():
    return render_template("liver_index.html")

