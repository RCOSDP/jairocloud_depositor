
import random
import string
import logging
from flask import Flask, render_template, redirect, url_for, request, flash, session ,current_app
from flask_login import login_user, LoginManager, current_user, logout_user
from flask_security import LoginForm, url_for_security
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,PasswordField
from config import MOCK_SHIB_DATA
from models import User as _User
from models import Affiliation_Id as _Affiliation_Id
from api import User
from api import Affiliation_Id
from db_setting import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://invenio:dbpass123@192.168.56.111:25401/invenio'
app.logger.setLevel(logging.INFO)
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)

class LoginForm(FlaskForm):
    email = StringField('メールアドレス')
    password = PasswordField('パスワード')
    submit = SubmitField('ログイン')

@app.route("/login", methods=['GET'])
def index_login():
    # login_user()
    # if not current_user:
    #     return render_template("login_index.html")
    # return index_item()
    csrf_random = generate_random_str(length=64)
    session['csrf_random'] = csrf_random
    login_user_form = LoginForm()
    return render_template("login_index.html", login_user_form = login_user_form)

@login_manager.user_loader
def load_user(user_id):
    user=User().get_user_by_id(user_id)
    return user

@app.route("/login", methods=['POST'])
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
                app.logger.info("login id:",user.user_id)
                return url_for("index_item")
    flash("Missing SHIB_ATTRs!", category='error')
    return index_login()


@app.route("/logout", methods=['GET'])
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

@app.route("/affiliation_setting")
def index_affili():
    form = FlaskForm(request.form)
    return render_template("affi_index.html",form = form)

@app.route("/item_register")
def index_item():
    form = FlaskForm(request.form)
    return render_template("item_index.html",form = form)
    