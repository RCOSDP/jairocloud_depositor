from mock import patch,MagicMock
import pytest
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session ,current_app, jsonify, Blueprint, json,make_response
from flask_login import login_user, current_user, logout_user, login_required,LoginManager
from flask_wtf import FlaskForm
from sqlalchemy_utils.functions import create_database, database_exists, drop_database
from depositor_admin_setting import AdminSettingApp
from depositor_item_register import ItemRegisterApp
from depositor_login import LoginApp
from depositor_models.db_setting import db as db_
from depositor_models.db_setting import DATABASE_URI, init_db
from depositor_models.user import User, User_manager
from depositor_models.affiliation_id import Affiliation_Id, Affiliation_Id_manager
from depositor_models.affiliation_repository import Affiliation_Repository, Affiliation_Repository_manager
from depositor_login.views import index_login


def test_index_affili(app, db, users, client,mocker,Affiliation_Id_settings,Affiliation_Repository_settings):
    url = "/admin_setting/"
    #no login
    with app.test_request_context(url):
            res = app.test_client().get(url)
            assert res.status_code == 302
            assert res.location == url_for('login.index_login')
            

    #一般ユーザー
    user = User_manager.get_user_by_id(2)
    mock_render = mocker.patch("depositor_admin_setting.views.render_template", return_value=make_response())
    with app.test_request_context(url):
            login_user(user)
            res = app.test_client().get(url)
            assert res.status_code == 200
            args, kwargs = mock_render.call_args
            assert args[0] == "admin_setting/permission_required.html"
            
    #get

    #管理者
    user = User_manager.get_user_by_id(0)
    repository_list = Affiliation_Id_manager.get_affiliation_id_list()
    aff_repository = {"-1": {"access_token": "default_token", "repository_url": "https://example/repository_url/default"}, "101": {"access_token": "test_token", "repository_url": "https://example/repository_url/test"}}
    mock_render = mocker.patch("depositor_admin_setting.views.render_template", return_value=make_response())
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().get(url)
        assert res.status_code == 200
        args, kwargs = mock_render.call_args
        assert args[0] == "admin_setting/affi_index.html"
        assert kwargs["affiliation_id_list"] == repository_list
        assert kwargs["aff_repository_dict"] == json.dumps(aff_repository)
        assert kwargs["affiliation_name"] == "default"
        assert kwargs["repository_url"] == "https://example/repository_url/default"
        assert kwargs["access_token"] == "default_token"


    #図書館員
    user = User_manager.get_user_by_id(1)
    repository_list = Affiliation_Id_manager.get_affiliation_id_list()
    aff_repository = {"-1": {"access_token": "default_token", "repository_url": "https://example/repository_url/default"}, "101": {"access_token": "test_token", "repository_url": "https://example/repository_url/test"}}
    mock_render = mocker.patch("depositor_admin_setting.views.render_template", return_value=make_response())
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().get(url)
        assert res.status_code == 200
        args, kwargs = mock_render.call_args
        assert args[0] == "admin_setting/affi_index.html"
        assert kwargs["affiliation_id_list"] == repository_list
        assert kwargs["aff_repository_dict"] == json.dumps(aff_repository)
        assert kwargs["affiliation_name"] == "affiliation_test"
        assert kwargs["repository_url"] == 'https://example/repository_url/test'
        assert kwargs["access_token"] == "test_token"

    #Exception
    user = User_manager.get_user_by_id(0)
    with app.test_request_context(url):
        with patch("depositor_admin_setting.views.Affiliation_Repository_manager.get_aff_repository_by_affiliation_id",side_effect=Exception("test_error")):
            login_user(user)
            res = app.test_client().get(url)
            assert res.status_code == 400

    #post
    
    #管理者
    #項目が空
    user = User_manager.get_user_by_id(0)
    data = {"affiliation_name":"-1","repository_url":"","access_token":""}
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().post(url,json=data)
        assert res.status_code == 400

    #Affiliation_Repository更新
    user = User_manager.get_user_by_id(0)
    data = {"affiliation_name":"-1","repository_url":"https://example/repository_url/default/update","access_token":"update_default_token"}
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().post(url,json=data)
        assert res.status_code == 200
        setting = Affiliation_Repository_manager.get_aff_repository_by_affiliation_id(-1)
        assert setting.repository_url == "https://example/repository_url/default/update"
        assert setting.access_token == "update_default_token"

    #図書館員 affiliation_id=1
    #Affiliation_Repository更新
    user = User_manager.get_user_by_id(1)
    data = {"affiliation_name":"affiliation_test","repository_url":"https://example/repository_url/test/update","access_token":"update_test_token"}
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().post(url,json=data)
        assert res.status_code == 200
        setting = Affiliation_Repository_manager.get_aff_repository_by_affiliation_id(101)
        assert setting.repository_url == "https://example/repository_url/test/update"
        assert setting.access_token == "update_test_token"

    #管理者
    #Affiliation_Repository新規登録
    user = User_manager.get_user_by_id(0)
    data = {"affiliation_name":"103","repository_url":"https://example/repository_url/test3","access_token":"test_token3"}
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().post(url,json=data)
        assert res.status_code == 200
        setting = Affiliation_Repository_manager.get_aff_repository_by_affiliation_id(103)
        assert setting.repository_url == "https://example/repository_url/test3"
        assert setting.access_token == "test_token3"

    #図書館員 affiliation_id=2
    #Affiliation_Repository新規登録
    user = User_manager.get_user_by_id(4)
    data = {"affiliation_name":"affiliation_test2","repository_url":"https://example/repository_url/test2","access_token":"test_token2"}
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().post(url,json=data)
        assert res.status_code == 200
        setting = Affiliation_Repository_manager.get_aff_repository_by_affiliation_id(102)
        assert setting.repository_url == "https://example/repository_url/test2"
        assert setting.access_token == "test_token2"

    #管理者
    #Affiliation_IDに未登録
    user = User_manager.get_user_by_id(0)
    data = {"affiliation_name":"404","repository_url":"https://example/repository_url/test404","access_token":"test_token404"}
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().post(url,json=data)
        assert res.status_code == 400

    #図書館員
    #Affiliation_IDに未登録
    user = User_manager.get_user_by_id(1)
    data = {"affiliation_name":"affiliation_test404","repository_url":"https://example/repository_url/test404","access_token":"test_token404"}
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().post(url,json=data)
        assert res.status_code == 400

    #Exception
    user = User_manager.get_user_by_id(0)
    data = {"affiliation_name":"-1","repository_url":"https://example/repository_url/default/update","access_token":"update_default_token"}
    with app.test_request_context(url):
        with patch("depositor_admin_setting.views.Affiliation_Repository_manager.upt_aff_repository",side_effect=Exception("test_error")):        
            login_user(user)
            res = app.test_client().post(url,json=data)
            assert res.status_code == 400
    

def test_add_affili(app, db, users, client,mocker,Affiliation_Id_settings,Affiliation_Repository_settings):
    url = "/admin_setting/add"
    #no login
    with app.test_request_context(url):
            res = app.test_client().get(url)
            assert res.status_code == 302
            assert res.location == url_for('login.index_login')

    #get
    #管理者以外
    user = User_manager.get_user_by_id(1)
    mock_render = mocker.patch("depositor_admin_setting.views.render_template", return_value=make_response())
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().get(url)
        assert res.status_code == 200
        args,kwargs = mock_render.call_args
        assert args[0] == "admin_setting/permission_required.html"
    
    #管理者
    user = User_manager.get_user_by_id(0)
    mock_render = mocker.patch("depositor_admin_setting.views.render_template", return_value=make_response())
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().get(url)
        assert res.status_code == 200
        args,kwargs = mock_render.call_args
        assert args[0] == "admin_setting/add_affili.html"

    #post
    user = User_manager.get_user_by_id(0)
    data = {"affiliation_name":"affiliation_test4","affiliation_idp_url":"https://example/idp_url/test4"}
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().post(url,json=data)
        assert res.status_code == 200
        setting = Affiliation_Id_manager.get_affiliation_id_by_affiliation_name("affiliation_test4")
        assert setting.affiliation_name == "affiliation_test4"
        assert setting.affiliation_idp_url == "https://example/idp_url/test4"

    #Affiliation_ID登録済み
    user = User_manager.get_user_by_id(0)
    data = {"affiliation_name":"affiliation_test","affiliation_idp_url":"https://example/idp_url/test5"}
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().post(url,json=data)
        assert res.status_code == 400    
    
    user = User_manager.get_user_by_id(0)
    data = {"affiliation_name":"affiliation_test5","affiliation_idp_url":"https://example/idp_url/test"}
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().post(url,json=data)
        assert res.status_code == 400

    user = User_manager.get_user_by_id(0)
    data = {"affiliation_name":"affiliation_test","affiliation_idp_url":"https://example/idp_url/test"}
    with app.test_request_context(url):
        login_user(user)
        res = app.test_client().post(url,json=data)
        assert res.status_code == 400

    #Exception
    user = User_manager.get_user_by_id(0)
    data = {"affiliation_name":"affiliation_test5","affiliation_idp_url":"https://example/idp_url/test5"}
    with app.test_request_context(url):
        with patch("depositor_admin_setting.views.Affiliation_Id_manager.create_affiliation_id",side_effect=Exception("test_error")):
            login_user(user)
            res = app.test_client().post(url,json=data)
            assert res.status_code == 400