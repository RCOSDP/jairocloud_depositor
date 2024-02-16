import base64
import zipfile
import io
import os
import uuid
from flask import Flask, render_template, redirect, url_for, request, flash, session ,current_app, jsonify, Blueprint
from flask_login import login_user, current_user, logout_user
from flask_security import LoginForm, url_for_security
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,PasswordField
from modules.config import MOCK_SHIB_DATA
from modules.models import User as _User
from modules.models import Affiliation_Id as _Affiliation_Id
from .utils import dicttoxmlforsword # zip_folder

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

    """
    post_dataの例:
    {"item_metadata;{}, "contentfiles": [{"name":"file.png", "base64":"aaaaa"}, "thumbneil":[{"name":"thumb.png", "base64":"bbbb"}] ]}
    """
    try :
        current_app.logger.info("はじまり")
        current_app.logger.info(request)
        
        post_data = request.get_json(True,True,True)
        
        current_app.logger.info("jsonのowari")
        contenfiles=[]
        thumbnail=[]
    except Exception as ex:
        current_app.logger.info(ex)
    # current_app.logger.info(post_data)
    # with io.BytesIO() as mem_zip:
    #     current_app.logger.info("mem_zip")
    #     with zipfile.ZipFile("test.zip", mode="w") as zipf: #zipファイル確認のため"test.zip"だが本来はmem_zip
    #         current_app.logger.info("zipf")
    #         xmltree = dicttoxmlforsword("jpcoar2.0", post_data.get("item_metadata"))
    #         current_app.logger.info("aaaaaaaaaaa")
    #         zipf.writestr("metadata.xml", xmltree)
    #         for file in post_data.get("contentfiles"):
    #             binary_data = base64.b64decode(file.get("base64", ""))
    #             zipf.writestr(file.get("name",""), binary_data)
        
    # 一時tmpフォルダにxml,その他ファイルを書きだす処理
    current_app.logger.info("uuidの始まり")
    tmp_path_for_xml = os.path.join("tmp","tmp-"+str(uuid.uuid4()))
    tmp_path = "./"+tmp_path_for_xml
    # フォルダ作成
    os.mkdir(tmp_path)
    current_app.logger.info("uuidのowari")
    
    # xml書き出し
    current_app.logger.info("xmlの始まり")
    xmltree = dicttoxmlforsword("jpcoar2.0", post_data.get("item_metadata"))
    current_app.logger.info("tmp_path_for_xml")
    current_app.logger.info(tmp_path_for_xml)
    xmltree.write(tmp_path_for_xml+"/metadata.xml", encoding="utf-8", xml_declaration=True)
    current_app.logger.info("tmp_path_for_xml終わり")
    
    # コンテンツファイル書き出し
    for file in post_data.get("contentfiles"):
        binary_data = base64.b64decode(file.get("base64", ""))
        file_path = os.path.join(tmp_path,file.get("name",""))
        current_app.logger.info(file_path)
        with open(file_path, 'wb') as f:
            f.write(binary_data)
    current_app.logger.info("終わり２")
    # サムネ書き出し
    for thumbnail in post_data.get("thumbnail"):
        binary_data = base64.b64decode(thumbnail.get("base64", ""))
        file_path = os.path.join(tmp_path,thumbnail.get("name",""))
        current_app.logger.info(file_path)
        with open(file_path, 'wb') as f:
            f.write(binary_data)
    current_app.logger.info("終わり３")

    # xmlとコンテンツファイルをzipにまとめる処理
    # zip_folder(tmp_path, tmp_path+"/forsender.zip"

    # current_userよりaffiliation_idをとってaffiliaiton_repositoryテーブルからリポジトリURLをとる処理
    # 設定されていない場合デフォルトURLをとる

    # 該当リポジトリのswordapiにzipとユーザー情報？を投げる処理
    # ここまでエラーなしだった場合、successfullyを返す。
    # エラーが起きたら、failedを返す。

    return jsonify(200)
 