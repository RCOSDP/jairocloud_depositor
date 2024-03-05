import pytest
import os
from flask import Flask, url_for
from flask_login import LoginManager
from sqlalchemy_utils.functions import create_database, database_exists, drop_database
from depositor_admin_setting import AdminSettingApp
from depositor_item_register import ItemRegisterApp
from depositor_login import LoginApp
from depositor_models.db_setting import db as db_
from depositor_models.db_setting import DATABASE_URI, init_db
from depositor_models.user import User, User_manager
from depositor_models.affiliation_id import Affiliation_Id, Affiliation_Id_manager
from depositor_models.affiliation_repository import Affiliation_Repository, Affiliation_Repository_manager

@pytest.fixture()
def base_app():
    app_ = Flask("testapp")
    login_manager = LoginManager()
    login_manager.init_app(app_)
    app_.config["SQLALCHEMY_DATABASE_URI"]=DATABASE_URI
    app_.config["TESTING"]="True"
    app_.config["SECRET_KEY"]="SECRET_KEY"
    AdminSettingApp(app_)
    ItemRegisterApp(app_)
    LoginApp(app_)
    
    @login_manager.user_loader
    def load_user(user_id):
        user=User_manager.get_user_by_id(user_id)
        return user
    return app_
    
@pytest.yield_fixture()    
def app(base_app):
    with base_app.app_context():
        yield base_app
      
@pytest.yield_fixture()    
def db(app):
    print()
    init_db(app)
    if not database_exists(DATABASE_URI):
        create_database(DATABASE_URI)
    db_.create_all()
    yield db_
    db_.session.remove()
    db_.drop_all()


@pytest.yield_fixture()
def client(app):
    """Get test client."""
    with app.test_client() as client:
        yield client

@pytest.fixture()
def users(app, db):
    test_admin = User(id=0, user_id="test_admin", affiliation_id=1, user_orcid = "test_admin", role = "管理者")
    test_cont = User(id=1, user_id="test_cont", affiliation_id=2, user_orcid = "test_cont", role = "図書館員")
    test_user_1 = User(id=2, user_id="test_user1A", affiliation_id=1, user_orcid = "test_user1", role = "")
    test_user_2 = User(id=3, user_id="test_user2A", affiliation_id=2, user_orcid = "test_user2", role = "")
    test_user_3 = User(id=4, user_id="test_user3", affiliation_id=3, user_orcid = "test_user3", role = "図書館員")
    test_user_4 = User(id=5, user_id="test_user4", affiliation_id=4, user_orcid = "test_user4", role = "")
    test_user_5 = User(id=6, user_id="test_user5", affiliation_id=5, user_orcid = "test_user5", role = "")
    
    
    User_manager.create_user(test_admin)
    User_manager.create_user(test_cont)
    User_manager.create_user(test_user_1)
    User_manager.create_user(test_user_2)
    User_manager.create_user(test_user_3)
    User_manager.create_user(test_user_4)
    User_manager.create_user(test_user_5)
    
    return [test_admin,
            test_cont,
            test_user_1,
            test_user_2,
            test_user_3,
            test_user_4,
            test_user_5]
    
@pytest.fixture()
def affiliation_ids(app, db):
    test_default = Affiliation_Id(id=0, affiliation_idp_url="-", affiliation_name ="default")
    test_alpha = Affiliation_Id(id=1, affiliation_idp_url="https://idp.auth.alphaalpha.ac.jp/idp/profile/SAML2/Redirect/SSO", affiliation_name ="alpha")
    
    Affiliation_Id_manager.create_affiliation_id(test_default)
    Affiliation_Id_manager.create_affiliation_id(test_alpha)
    
    return [test_default,
            test_alpha]
    
@pytest.fixture()
def affiliation_repositories(app, db):
    test_default = Affiliation_Repository(id = 1, affiliation_id=0, repository_url= "https://defaultdefault.ac.jp", access_token = "test")
    test_alpha = Affiliation_Repository(id = 2, affiliation_id=1, repository_url= "https://alphaalpha.ac.jp", access_token = "test")
    test_gamma = Affiliation_Repository(id = 3, affiliation_id=3, repository_url= "", access_token = "")
    test_delta = Affiliation_Repository(id = 4, affiliation_id=4, repository_url= "", access_token = "test")
    test_epsilon = Affiliation_Repository(id = 5, affiliation_id=5, repository_url= "https://deltadelta.ac.jp", access_token = "")
    
    Affiliation_Repository_manager.create_aff_repository(test_default)
    Affiliation_Repository_manager.create_aff_repository(test_alpha)
    Affiliation_Repository_manager.create_aff_repository(test_gamma)
    Affiliation_Repository_manager.create_aff_repository(test_delta)
    Affiliation_Repository_manager.create_aff_repository(test_epsilon)
    
    return [test_default,
            test_alpha,
            test_gamma,
            test_delta,
            test_epsilon]