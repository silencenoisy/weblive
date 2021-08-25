from app.models import User,Room,Danmu,RoomType,Give,GiveLevel,GiveLog,Subscription
from datetime import datetime, timedelta
import time

from app import rd,db,Config
import json


def allow_pic(filename):
    if '.' in filename:
        if filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS:
            return True
    return False

def usr_pwd_check(account, pwd):
    usr = User.query.filter_by(account=account).first()
    if usr is not None:
        if usr.check_pwd(pwd):
            return True
    else:
        usr = User.query.filter_by(phone=account).first()
        if usr and usr.check_pwd(pwd):
            return True
    return False


def get_usr_data(account):
    return User.query.filter_by(account=account).first()


def get_danmu_data(room_name, last_time):
    data = []
    if last_time is None:
        last_times = datetime.now() - timedelta(seconds=3)
    else:
        last_times = datetime.fromtimestamp(int(last_time))
    last_index = 0
    rrdata = rd.lrange(room_name, last_index, last_index + 10)
    flag = False
    new_time = last_times
    while rrdata:

        for danmu in rrdata:
            danmu = json.loads(danmu)
            # print(danmu['submit_time'])
            sub_time = datetime.strptime(danmu['submit_time'], "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0)
            if sub_time > new_time:
                new_time = sub_time
            if sub_time <= last_times:
                flag = True
                break
            one_danmu = {
                "account": danmu['account'],
                "username": danmu['username'],
                "content": danmu['content'],
                "evalue": danmu['evalue'],
                "cvalue":danmu['cvalue'],
                "submit_time": danmu['submit_time']
            }
            data.append(one_danmu)
        # print(data)
        if flag:
            break
        last_index += 10
        rrdata = rd.lrange(room_name, last_index, last_index + 10)
    new_time = int(time.mktime(new_time.timetuple()))
    return data, new_time


def set_danmu_data(data, usr):
    content = data.get('content')
    user_account = usr['account']
    usr = User.query.filter(User.account==user_account).first()
    usr.evalue+=1
    room_name = data.get('room_name')
    u_r = GiveLevel.query.filter(GiveLevel.room_id==Room.query.filter(Room.name==room_name).first().id,
                                 GiveLevel.user_id==usr.id).first()
    danmu_data = {
        "content": content,
        "user_id": usr.id,
        "account": usr.account,
        "username": usr.username,
        "evalue": usr.evalue,
        "cvalue":u_r.evalue if u_r is not None else 0,
        "room_name": room_name,
        "submit_time": str(datetime.now()),
    }
    return danmu_data, room_name

def set_give_danmu(roomname,usr,gives,give_num):
    u_r = GiveLevel.query.filter(GiveLevel.room_id == Room.query.filter(Room.name == roomname).first().id,
                                 GiveLevel.user_id == usr.id).first()
    danmu_data = {
        "content": usr.username+"赠送了主播"+str(give_num)+"个"+gives.name,
        "user_id": usr.id,
        "account": usr.account,
        "username": usr.username,
        "evalue": usr.evalue,
        "cvalue":u_r.evalue if u_r is not None else 0,
        "room_name": roomname,
        "submit_time": str(datetime.now()),
    }

    return danmu_data


def get_all_room_type():
    all_type = RoomType.query.all()
    data = []
    for live_type in all_type:
        temp = {
            "id":live_type.id,
            "name":live_type.name,
            "avarter":live_type.avarter,
            "mname":live_type.mname,
        }
        data.append(temp)
    return data

def save_danmu(data):
    room = Room.query.filter(Room.name==data['room_name']).first()
    danmu = Danmu(content=data['content'],user_id=data['user_id'],room_id=room.id,submit_time=data['submit_time'])
    db.session.add(danmu)
    db.session.commit()

def set_room_key(room):
    return room.name

def fetch_livers_data(type_name,page=1,per_page=20):
    # print("keys",rd.scard("zjyx"))
    # print(rd.srandmember("zjyx"))
    rdata = rd.srandmember(type_name,per_page)
    # print(rdata)
    data = []
    for liver in rdata:
        dliver = Room.query.filter_by(name=liver).first()
        if dliver is not None:
            usr = User.query.get(dliver.user_id)
            temp = {
                "room_name":dliver.name,
                "title":dliver.title,
                "liver":usr.username,
                "account":usr.account,
                "face":usr.face,
                "evalue":usr.evalue,
                'cover':dliver.cover,
                'type_id':dliver.type_id,
            }
            data.append(temp)

    return data

def send_give_data(roomname,usr,gives,give_num):
    room = Room.query.filter(Room.name==roomname).first()
    if room is not None:
        usr_room = GiveLevel.query.filter(GiveLevel.user_id==usr.id,GiveLevel.room_id==room.id).first()
        if usr_room is None:
            usr_room = GiveLevel(user_id=usr.id,room_id=room.id)

            db.session.add(usr_room)
            db.session.commit()
        give_values = gives.values*give_num
        usr_room.evalue+=give_values
        usr.money-=give_values
        give_log_add(usr.id,room.id,gives.id,give_num)
        db.session.commit()
        return True
    return False


def give_log_add(user_id,room_id,give_id,give_num):
    logs = GiveLog(user_id=user_id,room_id=room_id,type_id=give_id,num=give_num)
    db.session.add(logs)
    db.session.commit()


def sub_room(room,usr):
    if is_sub(room,usr,1):
        return True
    sub_rd = Subscription(room_id=room.id,user_id=usr.id)
    db.session.add(sub_rd)
    db.session.commit()
    return False



def is_sub(room,usr,del_rd=0):
    sub_rd = Subscription.query.filter(room.id == Subscription.room_id, usr.id == Subscription.user_id).first()
    if sub_rd is not None:
        if del_rd==1:
            db.session.delete(sub_rd)
            db.session.commit()
        return True
    return False

def get_sub_data(data):
    rdata = []
    for lroom in data:
        room = Room.query.filter(Room.id==lroom.room_id).first()
        is_live = rd.sismember("liver",room.name)
        temp = {
            "name":room.name,
            "title":room.title,
            "cover":room.cover,
            "is_live":is_live,
        }
        rdata.append(temp)

    return rdata

