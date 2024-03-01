
import logging
import sys
import os
from flask import Flask
from flask_login import LoginManager
from depositor_login.ext import LoginApp
from depositor_admin_setting.ext import AdminSettingApp
from depositor_item_register.ext import ItemRegisterApp
from depositor_models.db_setting import init_db
from depositor_models.user import User_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

HOST_NAME=os.environ.get("INVENIO_POSTGRESQL_HOST") #postgresql
DBNAME=os.environ.get("INVENIO_POSTGRESQL_DBNAME") #invenio
DBPASS=os.environ.get("INVENIO_POSTGRESQL_DBPASS") #dbpass123
DBUSER=os.environ.get("INVENIO_POSTGRESQL_DBUSER") #invenio

# 接続先DBの設定
app.config['SQLALCHEMY_DATABASE_URI'] = HOST_NAME+"://"+DBUSER+":"+DBPASS+"@"+HOST_NAME+":5432/"+ DBNAME
app.logger.setLevel(logging.INFO)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

init_db(app)
login_manager = LoginManager()
login_manager.init_app(app)

loginapp = LoginApp()
loginapp.init_app(app)
adminapp = AdminSettingApp()
adminapp.init_app(app)
itemregister = ItemRegisterApp()
itemregister.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user=User_manager.get_user_by_id(user_id)
    return user
