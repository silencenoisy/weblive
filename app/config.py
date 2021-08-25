import pymysql
import os
from datetime import timedelta
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://suser:qaz009299=@rm-bp1wrgx12de1zk5o53o.mysql.rds.aliyuncs.com/projectX'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = "this_is_a_key"
    PROPAGATE_EXCEPTIONS = True
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=5)
    XD_USER_DIR = "static/img"
    XD_BLOG_DIR = "static/img"
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), XD_USER_DIR)
    UPLOAD_FOLDER_BLOG = os.path.join(os.path.abspath(os.path.dirname(__file__)), XD_BLOG_DIR)
    # FC_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/users")
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
