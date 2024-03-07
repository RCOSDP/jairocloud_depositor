import pytest
import base64
import shutil
import os
from requests import Response
from mock import patch, MagicMock
from flask import session, url_for
from flask_login import current_user, login_user, logout_user
from depositor_login.views import generate_random_str,login
from depositor_models.user import User, User_manager
from depositor_models.affiliation_id import Affiliation_Id, Affiliation_Id_manager
from depositor_models.affiliation_repository import Affiliation_Repository, Affiliation_Repository_manager
from grobid_client.grobid_client import ServerUnavailableException

# ext.pyのcoverage用
def test_app_none(base_app_none):
    assert 1

def test_index_item(app, db, users):
    user = User_manager.get_user_by_id(1)
    with app.test_request_context("/item_register/"):
        # ログインしていない
        response = app.test_client().get("/item_register/")
        assert response.status_code == 302
        assert response.location == url_for('login.index_login')
        
        # ログインしている
        with patch("depositor_item_register.views.render_template") as render :
            login_user(user)
            response = app.test_client().get("/item_register/")
            render.assert_called()
    
def test_register(app, db, users, affiliation_ids, affiliation_repositories):
    def encode_to_base64(file_path):
        try:
            with open(file_path, "rb") as file:
                encoded_pdf = base64.b64encode(file.read())# .decode('utf-8')
            return encoded_pdf
        except FileNotFoundError:
            print("File not found.")
            return None
        
    alpha_user = users[0]
    beta_user = users[3]
    gamma_user = users[4]
    delta_user = users[5]
    epsilon_user = users[6]
    
    with app.test_request_context("/item_register/register"):
        # ログインしていない
        response = app.test_client().post("/item_register/register")
        assert response.status_code == 302
        assert response.location == url_for('login.index_login')
        
        login_user(beta_user)
        folder_path="./tests/tmp"
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        data = {"item_metadata":{}, 
                "contentfiles":[{"name":"france.png", "base64":encode_to_base64("./tests/data/france.png")}],
                "thumbnail":[{"name":"france.png", "base64":encode_to_base64("./tests/data/france.png")}]}
        with patch("flask.Request.get_json", return_value= data):
            mockresponse=Response()
            mockresponse.status_code = 200
            mockresponse._content = b'{"message": "Hello, world!"}'
            # ログインしているが、ユーザーのaffiliation_idではaff_repoが登録されていない。
            # tmpフォルダがない、contentsfile,thumbnailはついている　responseは404以外
            with patch("depositor_item_register.views.Affiliation_Repository_manager.get_aff_repository_by_affiliation_name") as get_aff_by_name:
                with patch("requests.post", return_value=mockresponse):
                    response = app.test_client().post("/item_register/register")
                    get_aff_by_name.assert_called()
                    assert response.status_code != 404 and response.status_code != 504
        
        # ログインしており、affiliation_idでaff_repoが登録されているがrepo_url,tokenが設定されていない。
        logout_user()
        login_user(gamma_user)
        data = {"item_metadata":{}, 
            "contentfiles":[],
            "thumbnail":[]}
        with patch("flask.Request.get_json", return_value= data):
            with patch("depositor_item_register.views.Affiliation_Repository_manager.get_aff_repository_by_affiliation_name") as get_aff_by_name:
                response = app.test_client().post("/item_register/register")
                get_aff_by_name.assert_called()
                assert response.status_code != 404

        # ログインしており、affiliation_idでaff_repoが登録されているがrepo_urlが設定されていない。
        logout_user()
        login_user(delta_user)
        data = {"item_metadata":{}, 
            "contentfiles":[],
            "thumbnail":[]}
        with patch("flask.Request.get_json", return_value= data):
            with patch("depositor_item_register.views.Affiliation_Repository_manager.get_aff_repository_by_affiliation_name") as get_aff_by_name:
                response = app.test_client().post("/item_register/register")
                get_aff_by_name.assert_called()
                assert response.status_code != 404
        
        # ログインしており、affiliation_idでaff_repoが登録されているがtokenが設定されていない。
        logout_user()
        login_user(epsilon_user)
        data = {"item_metadata":{}, 
            "contentfiles":[],
            "thumbnail":[]}
        with patch("flask.Request.get_json", return_value= data):
            with patch("depositor_item_register.views.Affiliation_Repository_manager.get_aff_repository_by_affiliation_name") as get_aff_by_name:
                response = app.test_client().post("/item_register/register")
                get_aff_by_name.assert_called()
                assert response.status_code != 404
                
        # ログインしており、affiliaton_idでaff_repoが登録されており、repo_url,access_tokenが設定されている。
        logout_user()
        login_user(alpha_user)
        with patch("flask.Request.get_json", return_value= data):
            with patch("depositor_item_register.views.Affiliation_Repository_manager.get_aff_repository_by_affiliation_name") as get_aff_by_name:
                response = app.test_client().post("/item_register/register")
                get_aff_by_name.assert_not_called()
                assert response.status_code != 404
    
        # 異常系 ステータスコードが404である。
        with patch("flask.Request.get_json", return_value= data):
            mockresponse=Response()
            mockresponse.status_code = 404
            mockresponse._content = b'{"message": "Hello, world!"}'
            with patch("depositor_item_register.views.Affiliation_Repository_manager.get_aff_repository_by_affiliation_name") as get_aff_by_name:
                with patch("requests.post", return_value=mockresponse):
                    response = app.test_client().post("/item_register/register")
                    get_aff_by_name.assert_not_called()
                    assert response.status_code == 404
                    
        # 異常系　Exception
        with patch("flask.Request.get_json", return_value= data):
            with patch("depositor_item_register.views.Affiliation_Repository_manager.get_aff_repository_by_affiliation_name") as get_aff_by_name:
                with patch("requests.post", side_effect=Exception()):
                    response = app.test_client().post("/item_register/register")
                    get_aff_by_name.assert_not_called()
                    assert response.status_code == 500
    
        
def test_pdf_reader(app, users):
    def encode_to_base64(file_path):
        try:
            with open(file_path, "rb") as file:
                encoded_pdf = base64.b64encode(file.read())# .decode('utf-8')
            return encoded_pdf
        except FileNotFoundError:
            print("File not found.")
            return None
        
    class MockGrobidClass(MagicMock):
        def process(a, b, c, **args):
            return 1
    user = users[0]
    with app.test_request_context("/item_register/pdf_reader"):
        # ログインしていない
        response = app.test_client().post("/item_register/pdf_reader")
        assert response.status_code == 302
        assert response.location == url_for('login.index_login')
        
        login_user(user)
        # ログインしている。正常系
        folder_path="./tests/tmp"
        os.makedirs("./tests/tmp/test/output/data")
        shutil.copy("./tests/data/test.grobid.tei.xml", "./tests/tmp/test/output/data")
        os.makedirs("./tests/tmp/test/data", exist_ok=True)
        shutil.copy("./tests/data/test.pdf", "./tests/tmp/test/data")
        data = {"item_metadata":{}, 
                "contentfiles":[{"name":"test.pdf", "base64":encode_to_base64("./tests/data/test.pdf")}]}
        with patch("flask.Request.get_json", return_value= data):
            with patch("uuid.uuid4", return_value="test"):
                with patch("depositor_item_register.views.GrobidClient", return_value = MockGrobidClass()):
                    with patch("os.mkdir"):
                        response = app.test_client().post("/item_register/pdf_reader")
                        assert response.status_code == 200
                        assert response.data.decode('unicode_escape') == '{"author":[{"creatorName":"De Marchis Cristiano","familyName":"De Marchis","givenName":"Cristiano"},{"creatorName":"Simon-Martinez Cristina","familyName":"Simon-Martinez","givenName":"Cristina"},{"creatorName":"Conforto Silvia","familyName":"Conforto","givenName":"Silvia"},{"creatorName":"Gharabaghi Alireza","familyName":"Gharabaghi","givenName":"Alireza"}],"date":{"type":"Available","value":"2016-03-08"},"lang":"en","publisher":"Springer Science and Business Media LLC","title":"Multi-contact functional electrical stimulation for hand opening: electrophysiologically driven identification of the optimal stimulation site"}\n'

        # 異常系　OSError   
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        data = {"item_metadata":{}, 
                "contentfiles":[{"name":"test.png", "base64":encode_to_base64("./tests/data/test.pdf")}]}
        with patch("flask.Request.get_json", return_value= data):
            with patch("uuid.uuid4", return_value="test"):
                with patch("depositor_item_register.views.GrobidClient", side_effect = MockGrobidClass()):
                    response = app.test_client().post("/item_register/pdf_reader")
                    assert response.status_code == 500
                    assert response.data.decode('unicode_escape') == '{"error":"PDFが適切ではない、またはPDFファイルが存在しない可能性があります。"}\n'

        # 異常系　ServerUnavailableException
        with patch("flask.Request.get_json", return_value= data):
            with patch("uuid.uuid4", return_value="test"):
                with patch("depositor_item_register.views.GrobidClient", side_effect = ServerUnavailableException()):
                    response = app.test_client().post("/item_register/pdf_reader")
                    assert response.status_code == 500
                    assert response.data.decode('unicode_escape') == '{"error":"PDF情報抽出機能との接続ができません。"}\n'
        
        # 異常系　Exception
        with patch("flask.Request.get_json", return_value= data):
            with patch("uuid.uuid4", return_value="test"):
                with patch("depositor_item_register.views.GrobidClient", side_effect = Exception()):
                    response = app.test_client().post("/item_register/pdf_reader")
                    assert response.status_code == 500