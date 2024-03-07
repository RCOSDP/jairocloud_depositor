from mock import patch,MagicMock
import pytest
from flask import session, url_for
from flask_login import current_user, login_user
from depositor_login.views import generate_random_str,login
from depositor_models.user import User, User_manager
from depositor_models.affiliation_id import Affiliation_Id, Affiliation_Id_manager

# ext.pyのcoverage用
def test_app_none(base_app_none):
    assert 1

def test_generate_random_str(app, db, users, client):
    assert len(generate_random_str()) == 128
    assert len(generate_random_str(91)) == 91
    
def test_top(app, db, users):
    user = User_manager.get_user_by_id(1)
    with app.test_request_context("/"):
        with patch("depositor_login.views.index_login") as index_login:
            login_user(user)
            response = app.test_client().get("/")
            index_login.assert_called()
        
def test_index_login(app, db, users):
    user = User_manager.get_user_by_id(1)
    with app.test_request_context("/login"):
        with patch("depositor_login.views.render_template") as render :
            response = app.test_client().get("/login")
            render.assert_called()
        login_user(user)
        response = app.test_client().get("/login")
        assert response.status_code == 302
        assert response.location == url_for('item_register.index_item')

def test_login(app, db, mocker):
    with app.test_request_context("/login"):
        # リクエストボディなし
        with patch("depositor_login.views.index_login") as index_login :
            response = app.test_client().post("/login")
            index_login.assert_called()
            
        # パスワードミス
        with patch("depositor_login.views.index_login") as index_login :
            with patch("flask_wtf.FlaskForm.validate_on_submit", return_value=True):
                request_data = {"email":"exam@exam.com", "password":"mistake"}
                response = app.test_client().post("/login", data=request_data)
                index_login.assert_called()
                
        # メールアドレスミス
        with patch("depositor_login.views.index_login") as index_login :
            with patch("flask_wtf.FlaskForm.validate_on_submit", return_value=True):
                request_data = {"email":"exam@exam.com", "password":"testpass"}
                response = app.test_client().post("/login", data=request_data)
                index_login.assert_called()
                
        # affiliation_idが見つからず、userも見つからない。
        with patch("depositor_login.views.index_login") as index_login :
            with patch("flask_wtf.FlaskForm.validate_on_submit", return_value=True):
                request_data = {"email":"testuser1A@nii.ac.jp", "password":"testpass"}
                response = app.test_client().post("/login", data=request_data)
                response.status_code == 302
                response.location == url_for("item_register.index_item")

        # affiliation_id、userが見つかる。    
        with patch("depositor_login.views.index_login") as index_login :
            with patch("flask_wtf.FlaskForm.validate_on_submit", return_value=True):
                create_user = mocker.patch("depositor_login.views.Affiliation_Id_manager.create_affiliation_id")
                create_aff_id = mocker.patch("depositor_login.views.User_manager.create_user")
                request_data = {"email":"testuser1A@nii.ac.jp", "password":"testpass"}
                response = app.test_client().post("/login", data=request_data)
                
                response.status_code == 302
                response.location == url_for("item_register.index_item")
                create_user.assert_not_called()
                create_aff_id.assert_not_called()
        

def test_logout(app, db, users):
    user = User_manager.get_user_by_id(1)
    with app.test_request_context("/logout"):
        with patch("depositor_login.views.logout_user") as logout :
            login_user(user)
            response = app.test_client().get("/logout")
            logout.assert_called()
            assert response.status_code == 302
            assert response.location == url_for('login.top')
     