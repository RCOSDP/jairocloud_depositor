
import random
import string
from flask import Flask, render_template, redirect, url_for, request, flash, session ,current_app, jsonify, Blueprint
from flask_login import login_user, current_user, logout_user
from flask_security import LoginForm, url_for_security
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,PasswordField
from .config import MOCK_SHIB_DATA
from depositor_models.user import User, User_manager
from depositor_models.affiliation_id import Affiliation_Id_manager

blueprint = Blueprint(
    "login",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static")

class LoginForm(FlaskForm):
    email = StringField('メールアドレス')
    password = PasswordField('パスワード')
    submit = SubmitField('ログイン')

@blueprint.route("", methods=['GET'])
def top():
    return index_login()

@blueprint.route("/login", methods=['GET'])
def index_login():
    import sys

    print(sys.path)
    if not current_user.is_anonymous:
        return redirect(url_for('item_register.index_item'))
    csrf_random = generate_random_str(length=64)
    session['csrf_random'] = csrf_random
    login_user_form = LoginForm()
    
    return render_template("login/login_index.html", login_user_form = login_user_form)

@blueprint.route("/login", methods=['POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        # shibbolethで返ってくる値を固定値とする。パスワードはtestpass固定
        if form.password.data == "testpass":
            shib_data = MOCK_SHIB_DATA.get(form.email.data)
            if shib_data :
                affiliation_idp_url = shib_data.get("affiliation_idp_url",None)
                affiliation_id = Affiliation_Id_manager().get_affiliation_id_by_idp_url(affiliation_idp_url)
                if not affiliation_id:
                    affiliation_name = shib_data.get("OrganizationName",None)
                    affiliation_id = Affiliation_Id_manager().create_affiliation_id(affiliation_idp_url=affiliation_idp_url,
                                                                      affiliation_name=affiliation_name)
                affiliation_id_id = affiliation_id.id
                user_id = shib_data.get("eduPersonPrincipalName",None)
                user=User_manager().get_user_by_user_id(user_id)
                if not user :
                    user_orcid = shib_data.get("eduPersonOrcid",None)
                    role = shib_data.get("wekoSocietyAffiliation", None)
                    user = User(
                        user_id = user_id,
                        affiliation_id = affiliation_id_id,
                        user_orcid = user_orcid,
                        role = role
                    )
                    User_manager().create_user(user)
                login_user(user)
                return redirect(url_for("item_register.index_item"))
    flash("Missing SHIB_ATTRs!", category='error')
    return index_login()


@blueprint.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login.top'))


def generate_random_str(length=128):
    """Generate secret key."""
    rng = random.SystemRandom()

    return ''.join(
        rng.choice(string.ascii_letters + string.digits)
        for _ in range(0, length)
    )
