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
from depositor_models.affiliation_id import Affiliation_Id, Affiliation_Id_manager
from depositor_models.affiliation_repository import Affiliation_Repository, Affiliation_Repository_manager
from depositor_models.user import User, User_manager

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

@pytest.fixture()
def base_app_none():
    app_=None
    AdminSettingApp(app_)
    ItemRegisterApp(app_)
    LoginApp(app_)
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
    test_admin = User(id=0, user_id="test_admin", affiliation_id=-1, user_orcid = "test_admin", role = "管理者")
    test_cont = User(id=1, user_id="test_cont", affiliation_id=101, user_orcid = "test_cont", role = "図書館員")
    test_user_1 = User(id=2, user_id="test_user1A", affiliation_id=101, user_orcid = "test_user1", role = "")
    test_user_2 = User(id=3, user_id="test_user2A", affiliation_id=102, user_orcid = "test_user2", role = "")
    test_user_3 = User(id=4, user_id="test_user3A", affiliation_id=102, user_orcid = "test_user2", role = "図書館員")
    test_user_4 = User(id=5, user_id="test_user4A", affiliation_id=103, user_orcid = "test_user3", role = "図書館員")
    
    User_manager.create_user(test_admin)
    User_manager.create_user(test_cont)
    User_manager.create_user(test_user_1)
    User_manager.create_user(test_user_2)
    User_manager.create_user(test_user_3)
    User_manager.create_user(test_user_4)
    
    return [test_admin,
            test_cont,
            test_user_1,
            test_user_2,
            test_user_3,
            test_user_4]

@pytest.fixture()
def Affiliation_Id_settings(db):
    settings = list()
    settings.append(Affiliation_Id(id=-1,affiliation_idp_url="-",affiliation_name="default"))
    settings.append(Affiliation_Id(id=101,affiliation_idp_url="https://example/idp_url/test",affiliation_name="affiliation_test"))
    settings.append(Affiliation_Id(id=102,affiliation_idp_url="https://example/idp_url/test2",affiliation_name="affiliation_test2"))
    settings.append(Affiliation_Id(id=103,affiliation_idp_url="https://example/idp_url/test3",affiliation_name="affiliation_test3"))
    db.session.add_all(settings)
    db.session.add_all(settings)
    db.session.commit()
    return settings

@pytest.fixture()
def Affiliation_Repository_settings(db):
    settings = list()
    settings.append(Affiliation_Repository(id=1001,affiliation_id=-1,repository_url="https://example/repository_url/default",access_token="default_token"))
    settings.append(Affiliation_Repository(id=1002,affiliation_id=101,repository_url="https://example/repository_url/test",access_token="test_token"))
    db.session.add_all(settings)
    db.session.commit()
    return settings