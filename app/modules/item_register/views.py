
import random
import string
import logging
import json
from flask import Flask, render_template, redirect, url_for, request, flash, session ,current_app, jsonify, Blueprint
from flask_login import login_user, current_user, logout_user
from flask_security import LoginForm, url_for_security
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,PasswordField
from modules.config import MOCK_SHIB_DATA
from modules.models import User as _User
from modules.models import Affiliation_Id as _Affiliation_Id

blueprint = Blueprint(
    "item_register",
    __name__,
    url_prefix="/item_register",
    template_folder="templates",
    static_folder="static")

@blueprint.route("/", methods=['GET'])
def index_item():
    form = FlaskForm(request.form)
    return render_template("item_register/item_index.html", form = form)
 