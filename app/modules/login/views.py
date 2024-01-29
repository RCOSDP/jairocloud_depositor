
import os
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
from modules.api import User
from modules.api import Affiliation_Id

blueprint = Blueprint(
    "login",
    __name__,
    url_prefix="/login",
    template_folder="templates",
    static_folder="/static")

class LoginForm(FlaskForm):
    email = StringField('メールアドレス')
    password = PasswordField('パスワード')
    submit = SubmitField('ログイン')

@blueprint.route("/", methods=['GET'])
def index_login():
    csrf_random = generate_random_str(length=64)
    session['csrf_random'] = csrf_random
    login_user_form = LoginForm()
    
    return render_template("login/login_index.html", login_user_form = login_user_form)

@blueprint.route("/", methods=['POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        # shibbolethで返ってくる値を固定値とする。パスワードはtestpass固定
        if form.password.data == "testpass":
            shib_data = MOCK_SHIB_DATA.get(form.email.data)
            if shib_data :
                affiliation_idp_url = shib_data.get("affiliation_idp_url",None)
                affiliation_id_id = Affiliation_Id().get_affiliation_id_by_idp_url(affiliation_idp_url).id
                if not affiliation_id_id:
                    affiliation_name = shib_data.get("OrganizationName",None)
                    _affili_id = Affiliation_Id().create_affiliation_id(affiliation_idp_url=affiliation_idp_url,
                                                                      affiliation_name=affiliation_name)
                    affiliation_id_id = _affili_id.id
                user_id = shib_data.get("eduPersonPrincipalName",None)
                user=User().get_user_by_user_id(user_id)
                if not user :
                    user_orcid = shib_data.get("eduPersonOrcid",None)
                    role = shib_data.get("wekoSocietyAffiliation", None)
                    user = _User(
                        user_id = user_id,
                        affiliation_id = affiliation_id_id,
                        user_orcid = user_orcid,
                        role = role
                    )
                    User().create_user(user)
                login_user(user)
                return redirect(url_for("item_register.index_item"))
    flash("Missing SHIB_ATTRs!", category='error')
    return index_login()


@blueprint.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return index_login()


def generate_random_str(length=128):
    """Generate secret key."""
    rng = random.SystemRandom()

    return ''.join(
        rng.choice(string.ascii_letters + string.digits)
        for _ in range(0, length)
    )
