from app import db
from uuid import uuid4
from datetime import datetime


class Test(db.Model):
    __tablename__ = "test"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    info = db.Column(db.Text)
    submit_time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "Test:%d %s %s" % (self.id, self.info, self.submit_time)


# 通用信息
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(12), unique=True)  # 唯一账号
    username = db.Column(db.String(100), nullable=False)  # 昵称
    password = db.Column(db.String(255), nullable=False)  # 密码
    face = db.Column(db.String(255))  # 头像
    sex = db.Column(db.SmallInteger, default=0)  # 性别(0保密，1男，2女)
    info = db.Column(db.Text)  # 个性签名
    phone = db.Column(db.BigInteger, unique=True)  # 手机号
    email = db.Column(db.String(255))  # 邮箱
    evalue = db.Column(db.BigInteger, default=0)  # 经验值
    money = db.Column(db.Integer,default=10000)     # 钱
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))  # 所属角色
    submit_time = db.Column(db.DateTime, default=datetime.now)  # 添加时间

    def hash_password(self,pwd):
        from werkzeug.security import generate_password_hash
        self.pwd = generate_password_hash(pwd)

    def check_pwd(self, pwdd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, pwdd)

    @staticmethod
    def create_pwd(pwd):
        from werkzeug.security import generate_password_hash
        return generate_password_hash(pwd)

    def __repr__(self):
        return "Role:%d %s %s" % (self.id, self.account, self.username)


# 角色类型
class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)  # 角色名称
    submit_time = db.Column(db.DateTime, default=datetime.now)  # 添加时间

    # user = db.relationship('app.models.User', backref='role')  # 外键管理管理员
    # auths = db.relationship('app.models.Auth_Role', backref='role')  # 外键管理管理员

    def __repr__(self):
        return "Role:%d %s" % (self.id, self.name)


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)  # 权限名称

    # roles = db.relationship('app.models.Auth_Role',backref='auth') # 外键管理权限

    def __repr__(self):
        return "Auth:%d %s" % (self.id, self.name)


# 权限与角色
class Auth_Role(db.Model):
    __tablename__ = "auth_role"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))  # 所属角色
    auth_id = db.Column(db.Integer, db.ForeignKey("auth.id"))  # 所属权限

    def __repr__(self):
        return "Auth:%d %d %d" % (self.id, self.role_id, self.auth_id)


class Room(db.Model):
    __tablename__ = "room"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # 房间名
    title = db.Column(db.String(100), default="欢迎来到直播间")  # 直播间标题
    cover = db.Column(db.String(255))  # 直播间封面
    push_key = db.Column(db.String(100), unique=True, nullable=False)  # 推流秘钥
    pull_key = db.Column(db.String(100), unique=True, nullable=False)  # 拉流秘钥
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),unique=True)   # 用户外键
    type_id = db.Column(db.Integer, db.ForeignKey("room_type.id"), unique=True,default=1)  # 类别外键

    @staticmethod
    def create_push_key():
        import random
        key=''.join(random.sample("abcdefghijklmnopqrstuvwxyz",random.randrange(8,16)))
        return key

    @staticmethod
    def create_pull_key():
        import random
        key=''.join(random.sample("abcdefghijklmnopqrstuvwxyz",random.randrange(8,16)))
        return key

    def __repr__(self):
        return "Room:%s %s %s %d" % (self.name, self.push_key, self.pull_key, self.user_id)


class Danmu(db.Model):
    __tablename__ = "danmu"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255))  # 弹幕内容
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 用户外键
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))  # 房间外键
    submit_time = db.Column(db.DateTime, default=datetime.now)  # 添加时间

class RoomType(db.Model):
    __tablename__ = "room_type"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100),unique=True) # 分类名称
    avarter = db.Column(db.String(255)) # 图片
    mname = db.Column(db.String(100),nullable=False) # 简称


    def __repr__(self):
        return "RoomType:%s"%self.name

class Give(db.Model):
    __tablename__ = "give"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255),unique=True)    # 礼物名称
    values = db.Column(db.Integer,nullable=False)   # 礼物价值


class GiveLog(db.Model):
    __tablename__ = "give_log"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 用户外键
    type_id = db.Column(db.Integer, db.ForeignKey("give.id"))  # 类别外键
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))  # 主播外键
    num = db.Column(db.Integer,default=1)   # 礼物数量
    submit_time = db.Column(db.DateTime, default=datetime.now)  # 添加时间


class GiveLevel(db.Model):
    __tablename__ = "give_level"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 用户外键
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))  # 主播外键
    evalue = db.Column(db.Integer,default=0)    # 亲密度

    def __repr__(self):
        return "GiveLevel:%d %d evalue:%d"%(self.user_id,self.room_id,self.evalue)

class Subscription(db.Model):
    __tablename__ = "subscript"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 用户外键
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))  # 主播外键
    submit_time = db.Column(db.DateTime, default=datetime.now)  # 添加时间


if __name__ == "__main__":
    # db.drop_all()
    db.create_all()
    # room = Room(name="pig",push_key=Room.create_push_key(),pull_key=Room.create_pull_key(),user_id=1)
    # db.session.add(room)
    # db.session.commit()
    # role = Role(name="common_user")
    # auth = Auth(name="test1")
    # role_auth = Auth_Role(role_id=1,auth_id=1)
    # db.session.add(role)
    # db.session.add(auth)
    # db.session.commit()
    # db.session.add(role_auth)
    # db.session.commit()
    # user = User(account=12357,username="pigg",password=User.create_pwd("123456"),sex=0,info="sdsadsa",phone=15345678911,
    #             email="sdafv@qq.com",uuid=uuid4().hex,role_id=1)
    # db.session.add(user)
    # db.session.commit()
    pass
