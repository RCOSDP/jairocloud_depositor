import base64
import zipfile
import io
import os
import uuid
import requests
from flask import Flask, render_template, redirect, url_for, request, flash, session ,current_app, jsonify, Blueprint
from flask_login import login_user, current_user, logout_user
from flask_security import LoginForm, url_for_security
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,PasswordField
from modules.config import MOCK_SHIB_DATA
from modules.models import User as _User
from modules.models import Affiliation_Id as _Affiliation_Id
from modules.api import Affiliation_Repository, User
from .utils import dicttoxmlforsword # zip_folder

blueprint = Blueprint(
    "item_register",
    __name__,
    url_prefix="/item_register",
    template_folder="templates",
    static_folder="static")

@blueprint.route("/", methods=['GET'])
def index_item():
    if current_user.is_anonymous:
        return redirect(url_for('login.index_login'))
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
    
    post_data = request.get_json()
    
    tmp_zip_name = str(uuid.uuid4())+".zip"

    # app/tmpディレクトリがないなら生成
    if not(os.path.exists(os.path.join('./', 'tmp'))):
        os.mkdir("./tmp")
    with zipfile.ZipFile("tmp/"+tmp_zip_name, mode="w") as zipf:
        # xml書き出し
        xml_string = dicttoxmlforsword("jpcoar2.0", post_data.get("item_metadata"))
        zipf.writestr("data/metadata.xml", xml_string)
        
        # コンテンツファイル書き込み
        for file in post_data.get("contentfiles"):
            binary_data = base64.b64decode(file.get("base64", ""))
            zipf.writestr("data/contentfiles/"+file.get("name",""), binary_data)
            
        # サムネイル書き込み
        for file in post_data.get("thumbnail"):
            binary_data = base64.b64decode(file.get("base64", ""))
            zipf.writestr("data/thumbnail/"+file.get("name",""), binary_data)
            
    # current_userよりaffiliation_idをとってaffiliaiton_repositoryテーブルからリポジトリURLをとる処理
    current_affiliation_id = current_user.affiliation_id
    aff_repository = Affiliation_Repository().get_aff_repository_by_affiliation_id(current_affiliation_id)
    #　設定されている場合
    if aff_repository and not(aff_repository.repository_url=="" or aff_repository.access_token==""):
        repository_url=aff_repository.repository_url
        access_token=aff_repository.access_token
    # 設定されていない場合デフォルトURLをとる。いまはしらない。
    else:
        aff_repository = Affiliation_Repository().get_aff_repository_by_affiliation_name("default")
        repository_url=aff_repository.repository_url
        access_token=aff_repository.access_token
    
    sword_api_url = repository_url+"/sword/service-document"
    
    # 送信するデータ（辞書形式）
    data = {
        'file': '@'+tmp_zip_name+";type=application/zip"
    }

    # ヘッダーを定義
    headers = {
        'Authorization': 'Bearer '+access_token,
        'Content-Disposition': 'attachment; filename='+tmp_zip_name,
        "Packaging":"http://purl.org/net/sword/3.0/package/SimpleZip",
    }

    # 送信するファイル
    files = {'file': open('tmp/'+tmp_zip_name, 'rb')}  # ファイルのパスを指定してファイルを開く

    # POSTリクエストを送信
    # 該当リポジトリのswordapiにzipを投げる処理
    try:
        # current_app.logger.info(sword_api_url)
        # current_app.logger.info(data)
        # current_app.logger.info(headers)
        # current_app.logger.info(files)
        response = requests.post(url=sword_api_url, data=data, headers=headers, files=files)
    except requests.exceptions.RequestException as ex:
        current_app.logger.info(ex)
        return jsonify({"error":str(ex)}), 504
    finally:
        current_app.logger.info("一時zipファイル削除:"+tmp_zip_name)
        os.remove('tmp/'+tmp_zip_name)
    # レスポンスを処理
    
    # ここまでエラーなしだった場合、successfullyを返す。
    # エラーが起きたら、failedを返す。

    return jsonify(response.json())
 