import os

from . import api
from app.models import Test,Room,RoomType,Give,GiveLevel,GiveLog,Subscription
from app import db,conn,jwt,rd,Config

from flask import request,Response,jsonify,render_template,g
import urllib.parse
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,create_refresh_token,
)
import json
from uuid import uuid4
from .func import *
from .json_func import *
import random
from werkzeug.utils import secure_filename

#
# @jwt.user_claims_loader
# def add_claims_to_access_token(identity):
#     return {
#         'account': identity,
#         'auth': db.session.query("User.role_id").filter(User.account==identity).first()
#     }

@api.route("/refresh", methods=["POST"])
@jwt_required(refresh=True) # 刷新token的装饰器，这是最新的写法
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@api.route("/live/<roomname>",methods=['POST'])
def live_url(roomname):
    room = Room.query.filter(Room.name==roomname).first()

    if room is not None:
        # print(pull_key[0])
        liver = User.query.get(room.user_id)
        data = room_data_ret(room,liver)
        return json_ret(data)
    # print("error %s"%roomname)
    return json_ret({},"room not found",1)


@api.route('/auth', methods=['POST'])
def auth():
    # 打开数据库连接
    data = request.form
    url = data.get('swfurl')
    pull_key = data.get('name')
    if url and pull_key:
        lst_query = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        push_key = lst_query.get('key')
        if push_key is not None:
            room = Room.query.filter(Room.push_key==push_key,Room.pull_key==pull_key).first()
            types = RoomType.query.filter(RoomType.id==room.type_id).first()

            if room and types:
                rd.sadd("liver", set_room_key(room))
                rd.sadd(types.mname,set_room_key(room))
                return Response(response='success', status=200)  # 返回200状态码


    return Response(status=500)  # 返回500状态码

@api.route('/on_publish_done',methods=['POST'])
def on_publish_done():
    data = request.form
    url = data.get('swfurl')
    pull_key = data.get('name')
    if url and pull_key:
        lst_query = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        push_key = lst_query.get('key')

        if push_key is not None:
            room = Room.query.filter(Room.push_key == push_key, Room.pull_key == pull_key).first()
            types = RoomType.query.filter(RoomType.id == room.type_id).first()
            rd.srem("liver",set_room_key(room))
            rd.srem(types.mname, set_room_key(room))
            return Response(response='success',status=200)

    return Response(status=500)  # 返回500状态码

@api.route('/checkLogin',methods=['POST'])
def login_check():
    data = request.form
    account = data.get('username')
    pwd = data.get('password')
    if usr_pwd_check(account,pwd):
        usr = get_usr_data(account)
        usr_data = usr_data_ret(usr)
        token_data = {"account":account,"auth":usr.role_id}
        access_token = create_access_token(identity=token_data,fresh=True)
        refresh_token = create_refresh_token(token_data)
        next_url = data.get("next")
        # next_url = "/"
        if next_url:
            return jsonify(
                {"data": usr_data, "access_token": access_token, "refresh_token": refresh_token,"next":next_url, "code": 0, "msg": ""})
        return jsonify({"data":usr_data,"access_token":access_token,"refresh_token":refresh_token,"code":0,"msg":""})
    return json_ret({},"error",2)


@api.route('/usr',methods=['POST'])
@jwt_required()
def fetch_usr_data():
    userinfo = get_jwt_identity()
    usr = get_usr_data(userinfo['account'])
    usr_data=usr_data_ret(usr)
    return json_ret(usr_data)


@api.route('/register_port', methods=['POST'])
def register_port():
    data = request.form
    name = data.get('username')
    pwd = data.get('password')
    phone = data.get('phone')
    if name is not None and pwd is not None and phone is not None:
        users = User.query.filter(User.phone==phone).first()
        if users is not None:
            return json_ret({},"phone has exist",1001)
        usr = User(account=phone,username=name,password=User.create_pwd(pwd),phone=phone,uuid=uuid4().hex,role_id=1)
        db.session.add(usr)
        db.session.commit()
        usr_data = usr_data_ret(usr)
        token_data = {"account": usr.account, "auth": usr.role_id}
        access_token = create_access_token(identity=token_data, fresh=True)
        refresh_token = create_refresh_token(token_data)
        next_url = data.get("next")
        # next_url = "/"
        if next_url:
            return jsonify(
                {"data": usr_data, "access_token": access_token, "refresh_token": refresh_token, "next": next_url,
                 "code": 0, "msg": ""})
        return jsonify(
            {"data": usr_data, "access_token": access_token, "refresh_token": refresh_token, "code": 0, "msg": ""})
    return json_ret({}, "error", 2)


@api.route('/send_danmu', methods=['POST'])
@jwt_required()
def send_danmu():
    danmu_data = request.form
    if request.form is not None:
        usr_token_dt = get_jwt_identity()

        data,room_name = set_danmu_data(danmu_data,usr_token_dt)
        save_danmu(data)
        rd.lpush(room_name,json.dumps(data))
    return json_ret({})

@api.route('/fetch_danmu', methods=['POST'])
def fetch_danmu():
    qdata = request.form
    if qdata is not None:
        room_name = qdata.get('room_name')
        # danmu_num = qdata.get('danmu_num',10,int)
        last_time = qdata.get('last_time')
        if room_name is not None:
            data,new_time = get_danmu_data(room_name,last_time)
            return jsonify({"data":data,"new_time":new_time,"code":0,"msg":""})
    return json_ret([])


@api.route('/is_live',methods=['POST'])
def is_live_status():
    room_name = request.form.get('roomname')
    if room_name is not None:
        if rd.sismember("liver",room_name):
            return json_ret({"is_live":True})

        return json_ret({"is_live":False})
    return json_ret({},code=1,msg="error room_name")


@api.route("/room_all_type",methods=['GET','POST'])
def room_all_type():
    all_type = get_all_room_type()
    return json_ret(all_type)


@api.route("/livers",methods=['GET',"POST"])
def livers():
    if request.method=='GET':
        data = request.args
    else:
        data = request.form

    page = data.get("page",1,int)
    per_page = data.get("per_page",20,int)
    live_type = data.get("type_name")
    if live_type is not None:
        data = fetch_livers_data(live_type,page,per_page)
        livers_num = rd.scard(live_type)
        return jsonify({"data":data,"code":0,"msg":"","total":livers_num})
    return json_ret({})


@api.route("/changeHead",methods=['POST'])
@jwt_required()
def changeHead():
    uploads_pic = request.files['images']
    if uploads_pic and allow_pic(uploads_pic.filename):  # 文件不为空and文件格式正确
        filename = secure_filename(uploads_pic.filename)
        path = os.path.join(Config.UPLOAD_FOLDER, filename)
        uploads_pic.save(path)
        data = {'url': Config.XD_USER_DIR + '/' + filename}
        return json_ret(data)
    return json_ret(msg="error",code=500)

@api.route("/changeHeaded",methods=['POST'])
@jwt_required()
def changeHeaded():
    url = request.form['url']
    filename = url.split('/')[-1]
    print(filename)
    usr_data = get_jwt_identity()
    user = User.query.filter(User.account == usr_data["account"]).first()
    print(user)
    user.face = filename
    db.session.commit()
    return json_ret({})


@api.route("/username_change",methods=['POST'])
@jwt_required()
def username_change():
    change_data = request.form
    usr_data = get_jwt_identity()
    new_data = change_data['username']
    usr = User.query.filter(User.account == usr_data['account']).first()
    if new_data is not None and usr is not None:
        # 验证唯一性
        is_only = User.query.filter(User.username==new_data).first()
        if is_only is not None:
            return json_ret(msg="username has existed",code=55)

        usr.username = new_data
        db.session.commit()
        return json_ret({})

    return json_ret(msg="server error",code=500)

@api.route("/password_change",methods=['POST'])
@jwt_required()
def password_change():
    change_data = request.form
    usr_data = get_jwt_identity()
    new_data = change_data['password']
    usr = User.query.filter(User.account == usr_data['account']).first()
    if new_data is not None and usr is not None:
        # # 验证唯一性
        # is_only = User.query.filter(User.username==new_data).first()
        # if is_only is not None:
        #     return json_ret(msg="username has existed",code=55)

        usr.password = User.create_pwd(new_data)
        db.session.commit()
        return json_ret({})

    return json_ret(msg="server error",code=500)


@api.route("/email_change",methods=['POST'])
@jwt_required()
def email_change():
    change_data = request.form
    usr_data = get_jwt_identity()
    new_data = change_data['email']
    usr = User.query.filter(User.account == usr_data['account']).first()
    if new_data is not None and usr is not None:
        # # 验证唯一性
        # is_only = User.query.filter(User.username==new_data).first()
        # if is_only is not None:
        #     return json_ret(msg="username has existed",code=55)

        usr.email = new_data
        db.session.commit()
        return json_ret({})

    return json_ret(msg="server error",code=500)


@api.route("/info_change",methods=['POST'])
@jwt_required()
def info_change():
    change_data = request.form
    usr_data = get_jwt_identity()
    new_data = change_data['info']
    usr = User.query.filter(User.account == usr_data['account']).first()
    if new_data is not None and usr is not None:
        # # 验证唯一性
        # is_only = User.query.filter(User.username==new_data).first()
        # if is_only is not None:
        #     return json_ret(msg="username has existed",code=55)

        usr.info = new_data
        db.session.commit()
        return json_ret({})

    return json_ret(msg="server error",code=500)

@api.route("/sex_change",methods=['POST'])
@jwt_required()
def sex_change():
    change_data = request.form
    usr_data = get_jwt_identity()
    new_data = change_data['sex']
    usr = User.query.filter(User.account == usr_data['account']).first()
    if new_data is not None and usr is not None:
        # # 验证唯一性
        # is_only = User.query.filter(User.username==new_data).first()
        # if is_only is not None:
        #     return json_ret(msg="username has existed",code=55)

        usr.sex = new_data
        db.session.commit()
        return json_ret({})

    return json_ret(msg="server error",code=500)


@api.route("/get_live_key",methods=['POST'])
@jwt_required()
def live_key():
    usr_data = get_jwt_identity()
    usr = User.query.filter(User.account == usr_data['account']).first()
    if usr is not None:
        room = Room.query.filter(Room.user_id==usr.id).first()
        if room is not None:
            data = get_live_key(room)

        else:
            room = Room(name=usr.username,push_key=Room.create_push_key(),pull_key=Room.create_pull_key(),user_id=usr.id)
            db.session.add(room)
            db.session.commit()
            data = get_live_key(room)
        return json_ret(data)
    return json_ret(msg="error",code=500)

@api.route("/liver",methods=["GET",'POST'])
@jwt_required()
def liver_msg():
    usr_data = get_jwt_identity()
    usr = User.query.filter(User.account == usr_data['account']).first()
    if usr is not None:

        room = Room.query.filter(Room.user_id == usr.id).first()
        if room is not None:
            data = room_data_ret(room,usr)
            return json_ret(data)
    return json_ret(msg="server error",code=500)

@api.route("/title_change",methods=['POST'])
@jwt_required()
def live_title_change():
    change_data = request.form
    usr_data = get_jwt_identity()
    new_data = change_data['title']
    usr = User.query.filter(User.account == usr_data['account']).first()
    if new_data is not None and usr is not None:

        room = Room.query.filter(Room.user_id == usr.id).first()
        if room is not None:
        # # 验证唯一性
        # is_only = User.query.filter(User.username==new_data).first()
        # if is_only is not None:
        #     return json_ret(msg="username has existed",code=55)

            room.title = new_data
            db.session.commit()
            return json_ret({})

    return json_ret(msg="server error", code=500)


@api.route("/changeCover",methods=['POST'])
@jwt_required()
def changeCover():
    uploads_pic = request.files['images']
    if uploads_pic and allow_pic(uploads_pic.filename):  # 文件不为空and文件格式正确
        filename = secure_filename(uploads_pic.filename)
        path = os.path.join(Config.UPLOAD_FOLDER, filename)
        uploads_pic.save(path)
        data = {'url': Config.XD_USER_DIR + '/' + filename}
        return json_ret(data)
    return json_ret(msg="error",code=500)

@api.route("/changeCovered",methods=['POST'])
@jwt_required()
def changeCovered():
    url = request.form['url']
    filename = url.split('/')[-1]
    usr_data = get_jwt_identity()
    user = User.query.filter(User.account == usr_data["account"]).first()
    room = Room.query.filter(Room.user_id == user.id).first()
    if room:

        room.cover = filename
        db.session.commit()
        return json_ret({})

    return json_ret(msg="error",code=500)


@api.route("/type_change",methods=['POST'])
@jwt_required()
def live_type_change():
    change_data = request.form
    usr_data = get_jwt_identity()
    new_data = change_data['type_id']
    usr = User.query.filter(User.account == usr_data['account']).first()
    if new_data is not None and usr is not None:

        room = Room.query.filter(Room.user_id == usr.id).first()
        if room is not None:
        # # 验证唯一性
        # is_only = User.query.filter(User.username==new_data).first()
        # if is_only is not None:
        #     return json_ret(msg="username has existed",code=55)

            room.type_id = new_data
            db.session.commit()
            return json_ret({})

    return json_ret(msg="server error", code=500)

@api.route("/send_gives",methods=["POST"])
@jwt_required()
def send_gives():
    data = request.form
    usr_data = get_jwt_identity()
    roomname = data.get('roomname')
    give_id = data.get('give_id')
    give_num = data.get('num',1,int)
    account = usr_data['account']
    usr = User.query.filter(User.account == account).first()
    gives = Give.query.get(give_id)
    if gives is None:
        return json_ret(msg="give_id error",code=600)
    spend_value = gives.values*give_num
    if usr.money<spend_value:
        return json_ret(msg="lack money",code=5)
    if not send_give_data(roomname,usr,gives,give_num):
        return json_ret(msg="error",code=600)
    data = set_give_danmu(roomname,usr,gives,give_num)
    rd.lpush(roomname, json.dumps(data))
    return json_ret()

@api.route("/subscript",methods=["POST"])
@jwt_required()
def subscript_live():
    rdata = request.form
    roomname = rdata.get('roomname')
    room = Room.query.filter(Room.name == roomname).first()
    usr_data = get_jwt_identity()
    usr = User.query.filter(User.account==usr_data['account']).first()
    if room is not None:
        is_sub = sub_room(room,usr)
        data = {
            "is_subscript":not is_sub
        }
        return json_ret(data)

    return json_ret(msg="error",code=500)

@api.route("/is_subscript",methods=["POST"])
@jwt_required()
def is_subscript_live():
    rdata = request.form
    roomname = rdata.get('roomname')
    room = Room.query.filter(Room.name == roomname).first()
    usr_data = get_jwt_identity()
    usr = User.query.filter(User.account == usr_data['account']).first()
    if room is not None:
        is_subs = is_sub(room, usr)
        data = {
            "is_subscript": is_subs
        }
        return json_ret(data)

    return json_ret(msg="error",code=500)


@api.route("/usr/subscription",methods=["POST"])
@jwt_required()
def all_subscript_live():
    usr_data = get_jwt_identity()
    usr = User.query.filter(User.account==usr_data['account']).first()
    all_sub = Subscription.query.filter(Subscription.user_id==usr.id).all()
    data = get_sub_data(all_sub)
    return json_ret(data)
