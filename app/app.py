
import random
import string
from flask import Flask, render_template, redirect, url_for, request, flash, session ,current_app
from flask_login import login_user, LoginManager
from flask_security import LoginForm, url_for_security
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,PasswordField
from config import MOCK_SHIB_DATA
from models import User as _User
from models import Affiliation_Id as _Affiliation_Id
from api import User
from api import Affiliation_Id

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"

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

@app.route("/login", methods=['POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        shib_data = MOCK_SHIB_DATA.get(form.email.data)
        if shib_data and form.password.data == "testpass":
            affiliation_idp_url = shib_data.get("affiliation_idp_url",None)
            if not Affiliation_Id.get_affiliation_id_by_idp_url(affiliation_idp_url):
                _affili_id = _Affiliation_Id()
                Affiliation_Id.create_affiliation_id()
            user = _User(
                affiliation_id=
            )
            # login_user()
            return form.email.data
    flash("Missing SHIB_ATTRs!", category='error')
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
    return render_template("affi_index.html")

@app.route("/item_register")
def index_item():
    return render_template("item_index.html")
    