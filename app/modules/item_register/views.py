import base64
import zipfile
import io
import os
import shutil
import time
import uuid
import requests
import xml.etree.ElementTree as ET
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
from modules.grobid_client.grobid_client import GrobidClient

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
    current_app.logger.info(current_user.affiliation_id)
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
    current_app.logger.info("はじまり")
    # current_app.logger.info(request)
    
    post_data = request.get_json()
    
    current_app.logger.info("jsonのowari")
    tmp_zip_name = str(uuid.uuid4())+".zip"
    # current_app.logger.info(post_data)
    
    # メモリー内にzipファイルを作る処理
    current_app.logger.info("mem_zip")
        # zipファイル確認のため"test.zip"だが本来はmem_zipバッファ内でzip持ってるとファイル名を決められないのでやめます。
        # ex: with zipfile.ZipFile(mem_zip, mode="w") as zipf
    with zipfile.ZipFile("tmp/"+tmp_zip_name, mode="w") as zipf:
        current_app.logger.info("zipf")
        # xml書き出し
        current_app.logger.info("xmlの始まり")
        xml_string = dicttoxmlforsword("jpcoar2.0", post_data.get("item_metadata"))
        zipf.writestr("data/metadata.xml", xml_string)
        current_app.logger.info("xml終わり")
        
        # コンテンツファイル書き込み
        current_app.logger.info("コンテンツファイル始まり")
        for file in post_data.get("contentfiles"):
            binary_data = base64.b64decode(file.get("base64", ""))
            zipf.writestr("data/contentfiles/"+file.get("name",""), binary_data)
        current_app.logger.info("コンテンツファイル終わり")
            
        # サムネイル書き込み
        current_app.logger.info("サムネイル始まり")
        for file in post_data.get("thumbnail"):
            binary_data = base64.b64decode(file.get("base64", ""))
            zipf.writestr("data/thumbnail/"+file.get("name",""), binary_data)
        current_app.logger.info("サムネイル終わり")
            
    # current_userよりaffiliation_idをとってaffiliaiton_repositoryテーブルからリポジトリURLをとる処理
    current_affiliation_id = current_user.affiliation_id
    aff_repository = Affiliation_Repository().get_aff_repository_by_affiliation_id(current_affiliation_id)
    #　設定されている場合
    if aff_repository:
        repository_url=aff_repository.repository_url
        access_token=aff_repository.access_token
    # 設定されていない場合デフォルトURLをとる。いまはしらない。
    else:
        aff_repository = Affiliation_Repository().get_affiliation_id_by_affiliation_name("default")
        # 現在はまだデフォルトが何も決まっていないのでモックする。
        repository_url="https://repository.repo.nii.ac.jp"
        access_token="accessToken"
        # repository_url=aff_repository.repository_url
        # access_token=aff_repository.access_token
    
    sword_api_url = repository_url+"/sword/service-document"
    
    # 送信するデータ（辞書形式）
    data = {
        'file': '@'+tmp_zip_name+";type=application/zip"
    }

    # ヘッダーを定義
    headers = {
        'Authorization': 'Bearer '+access_token,
        'Content-Disposition': 'attachment; filename='+tmp_zip_name
    }

    # 送信するファイル
    files = {'file': open('tmp/'+tmp_zip_name, 'rb')}  # ファイルのパスを指定してファイルを開く

    # # POSTリクエストを送信
    try:
        # current_app.logger.info(sword_api_url)
        # current_app.logger.info(data)
        # current_app.logger.info(headers)
        # current_app.logger.info(files)
        response = requests.post(url=sword_api_url, data=data, headers=headers, files=files)
    except requests.exceptions.RequestException as ex:
        current_app.logger.info(ex)
        response = 400
    # レスポンスを処理
    
    # 該当リポジトリのswordapiにzipとユーザー情報？を投げる処理
    # ここまでエラーなしだった場合、successfullyを返す。
    # エラーが起きたら、failedを返す。
    current_app.logger.info(response)

    return jsonify(response)

@blueprint.route("/pdf_reader", methods=['POST'])
def pdf_reader():
    XMLNS="{http://www.tei-c.org/ns/1.0}"
    
    def read_title(data, root):
        for child in root:
            if child.tag.endswith("titleStmt"):
                data["title"] = child.find(f"{XMLNS}title").text
            else:
                read_title(data, child)
        return
    
    def read_date(data, root):
        for child in root:
            if child.tag.endswith("publicationStmt"):
                data["date"] = {}
                data["date"]["type"] = "Available"
                data["date"]["value"] = child.find(f"{XMLNS}date").attrib["when"]
            else:
                read_date(data, child)
        return
    
    def read_lang(data, root):
        for child in root:
            if child.tag.endswith("text"):
                for key, value in child.attrib.items():
                    if key.endswith("lang"):
                        data["lang"] = value
                        break
            else:
                read_lang(data, child)
        return
      
    def read_publisher(data, root):
        for child in root:
            if child.tag.endswith("publicationStmt"):
                data["publisher"] = child.find(f"{XMLNS}publisher").text
            else:
                read_publisher(data, child)
        return
      
    def read_author(data, root):
        for child in root:
            if child.tag.endswith("author"):
                name = child.find(f"{XMLNS}persName")
                if name:
                    author_data = {
                        "familyName":name.find(f"{XMLNS}surname").text,
                        "givenName":name.find(f"{XMLNS}forename").text
                    }
                    author_data["creatorName"] = author_data["familyName"] + " " + author_data["givenName"]
                    data["author"].append(author_data)
            else:
                read_author(data, child)
        return
      
    if current_user.is_anonymous:
        return redirect(url_for('login.index_login'))
    current_app.logger.info(current_user.affiliation_id)
    # get and save PDF
    post_data = request.get_json()
    file_uuid = str(uuid.uuid4())
    file_name = None
    file_path = os.path.join("tmp", file_uuid)
    output_path = os.path.join(file_path, "output")
    
    # seetup PDF from json
    os.mkdir(file_path)
    with zipfile.ZipFile(os.path.join(file_path, "contents.zip"), mode="w") as zipf:
        for file in post_data.get("contentfiles"):
            if file.get("name","").endswith(".pdf"):
                file_name = file.get("name","").replace(".pdf", ".grobid.tei.xml")
                binary_data = base64.b64decode(file.get("base64", ""))
                zipf.writestr(f"{file.get("name","")}", binary_data)
                break
    with zipfile.ZipFile(os.path.join(file_path, "contents.zip")) as zf:
        zf.extractall(f"{file_path}/data")
        
    # PDF to XML by Grobid
    client = GrobidClient(config_path="./config.json")
    client.process("processHeaderDocument", file_path, output=output_path, consolidate_citations=True, tei_coordinates=True, force=True)
    
    # read XML
    tree = ET.parse(f"{output_path}/data/{file_name}")
    root = tree.getroot()
    data = {}
    data["author"] = []
    read_title(data, root)
    read_lang(data, root)
    read_date(data, root)
    read_publisher(data, root)
    read_author(data, root)
    print(data)
    
    # remove tmp file
    shutil.rmtree(file_path)
    
    form = FlaskForm(request.form)
    return render_template("item_register/item_index.html", form = form, metadata = data)
