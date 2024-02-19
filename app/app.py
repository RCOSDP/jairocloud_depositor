
import random
import string
import logging
import json
from flask import Flask, render_template, redirect, url_for, request, flash, session ,current_app, jsonify
from flask_login import login_user, LoginManager
from flask_wtf import FlaskForm
from modules.config import MOCK_SHIB_DATA
from db_setting import init_db
from modules.login.ext import LoginApp
from modules.admin_setting.ext import AdminSettingApp
from modules.item_register.ext import ItemRegisterApp
from modules.api import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://invenio:dbpass123@192.168.56.111:25401/invenio'
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
    user=User().get_user_by_id(user_id)
    return user
