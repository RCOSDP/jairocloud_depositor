
from flask import Flask, render_template, redirect, url_for, request, flash, session ,current_app, jsonify, Blueprint
from flask_login import login_user, current_user, logout_user
from flask_security import LoginForm, url_for_security
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,PasswordField
from modules.config import MOCK_SHIB_DATA
from modules.models import User as _User
from modules.models import Affiliation_Id as _Affiliation_Id
from .utils import dicttoxmlforsword

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


@blueprint.route("/register", methods=['POST'])
def register():
    # まだ、リクエストする方ができていないのでモック
    # 想定としては入力されたアイテムのメタデータ項目がrequestで投げられる。
    # また、ファイルがアップロードされている場合、/tmpに挙げられているものとする。
    post_data = request.get_json()
    metadata={}
    current_app.logger.info(post_data)
    
    # item_metadataをxml化する処理
    xmltree = dicttoxmlforsword("jpcoar2.0", post_data)

    # ファイル情報、特に本文URLが設定されている場合にコンテンツファイルのパスを持ってくる処理

    # xmlとコンテンツファイルをzipにまとめる処理

    # current_userよりaffiliation_idをとってaffiliaiton_repositoryテーブルからリポジトリURLをとる処理
    # 設定されていない場合デフォルトURLをとる

    # 該当リポジトリのswordapiにzipとユーザー情報？を投げる処理
    # ここまでエラーなしだった場合、successfullyを返す。
    # エラーが起きたら、failedを返す。

    return jsonify(metadata)
 