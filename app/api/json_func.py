from flask import jsonify
from app.models import User,Room


def json_ret(data={},msg="",code=0):
    return jsonify({"code":code,"msg":msg,"data":data})


def usr_data_ret(usr:User):
    if usr is not None:
        data = {
            "account":usr.account,  # 账号
            "username":usr.username,    # 用户名
            "face":usr.face,    # 头像
            "sex": usr.sex,     # 性别
            "info" :usr.info,  # 个性签名
            "phone" :usr.phone,  # 手机号
            "email" :usr.email, # 邮箱
            "evalue" :usr.evalue,  # 经验值
            "role_id" :usr.role_id  # 所属角色
        }
        return data
    return None

def room_data_ret(room:Room,usr:User):
    if room is not None and usr is not None:
        data = {
            'title':room.title,
            'url':room.pull_key,
            'face':usr.face,
            'liver':usr.username,
            'account':usr.account,
            'cover':room.cover,
            'type_id':room.type_id,
        }
        return data
    return None


def get_live_key(room):
    data = {
        "pushkey":room.push_key,
        "pullkey":room.pull_key,
        "roomname":room.name,
    }
    return data