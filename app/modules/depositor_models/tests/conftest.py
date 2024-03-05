import pytest
import os
from flask import Flask, url_for
from sqlalchemy_utils.functions import create_database, database_exists, drop_database
from depositor_admin_setting import AdminSettingApp
from depositor_item_register import ItemRegisterApp
from depositor_login import LoginApp
from depositor_models.db_setting import db as db_
from depositor_models.db_setting import DATABASE_URI, init_db

@pytest.fixture()
def base_app():
    app_ = Flask("testapp")
    app_.config["SQLALCHEMY_DATABASE_URI"]=DATABASE_URI
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
