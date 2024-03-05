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
from flask_wtf import FlaskForm
from grobid_client.grobid_client import GrobidClient, ServerUnavailableException
from depositor_models.affiliation_repository import Affiliation_Repository_manager
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
    if current_user.is_anonymous:
        return redirect(url_for('login.index_login'))
    tmp_file_path = os.environ.get("TMPORARY_FILE_PATH")
    
    post_data = request.get_json()
    
    tmp_zip_name = str(uuid.uuid4())+".zip"

    # app/tmpディレクトリがないなら生成
    if not(os.path.exists(tmp_file_path)):
        os.mkdir(tmp_file_path)
    with zipfile.ZipFile(tmp_file_path+tmp_zip_name, mode="w") as zipf:
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
    aff_repository = Affiliation_Repository_manager.get_aff_repository_by_affiliation_id(current_affiliation_id)
    #　設定されている場合
    if aff_repository and not(aff_repository.repository_url=="" or aff_repository.access_token==""):
        repository_url=aff_repository.repository_url
        access_token=aff_repository.access_token
    else:
        aff_repository = Affiliation_Repository_manager.get_aff_repository_by_affiliation_name("default")
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
    files = {'file': open(tmp_file_path+tmp_zip_name, 'rb')}  # ファイルのパスを指定してファイルを開く

    # POSTリクエストを送信
    # 該当リポジトリのswordapiにzipを投げる処理
    try:
        # current_app.logger.info(sword_api_url)
        # current_app.logger.info(data)
        # current_app.logger.info(headers)
        # current_app.logger.info(files)
        response = requests.post(url=sword_api_url, data=data, headers=headers, files=files, verify=False)
        if response.status_code == 404:
            return response.text, 404
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as ex:
        current_app.logger.info(str(ex))
        return jsonify({"error":str(ex)}), 504
    finally:
        current_app.logger.info("一時zipファイル削除:"+tmp_zip_name)
        os.remove(tmp_file_path+tmp_zip_name)
    # レスポンスを処理
    
    # ここまでエラーなしだった場合、successfullyを返す。
    # エラーが起きたら、failedを返す。
    

    return jsonify(response.json())

@blueprint.route("/pdf_reader", methods=['POST'])
def pdf_reader():
    tmp_file_path = os.environ.get("TMPORARY_FILE_PATH")
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
    print("pdf read")
    if current_user.is_anonymous:
        return redirect(url_for('login.index_login'))
    current_app.logger.info(current_user.affiliation_id)
    # get and save PDF
    try:
        post_data = request.get_json()
        file_uuid = str(uuid.uuid4())
        file_name = None
        file_path = os.path.join("tmp", file_uuid)
        output_path = os.path.join(file_path, "output")
        
        # seetup PDF from json
        if not(os.path.exists(tmp_file_path)):
            os.mkdir(tmp_file_path)
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
        client = GrobidClient(config_path="./app/config.json")
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
        
        return jsonify(data), 200
    except OSError as ex:
        current_app.logger.info(str(ex))
        return jsonify({"error":"PDFが適切ではない、またはPDFファイルが存在しない可能性があります。"}), 500
    except ServerUnavailableException as ex:
        current_app.logger.info(str(ex))
        return jsonify({"error":"PDF情報抽出機能との接続ができません。"}), 500
    except Exception as ex:
        current_app.logger.info(str(ex))
        return jsonify({"error":str(ex)}), 500
    finally:
        # remove tmp file
        print(file_path)
        shutil.rmtree(file_path)
    
