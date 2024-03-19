from mock import patch,MagicMock
import pytest
from depositor_models.affiliation_repository import Affiliation_Repository, Affiliation_Repository_manager
from depositor_models.affiliation_id import Affiliation_Id, Affiliation_Id_manager

def test_Affiliation_Repository_manager(app, db):
    
    aff_idp_url_1 = "https://idp.auth.alphaalpha.ac.jp/idp/profile/SAML2/Redirect/SSO"
    test_affiliation_id_1 = Affiliation_Id(id=1, affiliation_idp_url=aff_idp_url_1, affiliation_name="alpha")
    # 正常系
    Affiliation_Id_manager.create_affiliation_id(test_affiliation_id_1)
    
    manager = Affiliation_Repository_manager()
    aff_url_1 = "https://idp.auth.alphaalpha.ac.jp"
    aff_url_2 = "https://idp.auth.betabeta.ac.jp"
    test_affiliation_repository_1 = Affiliation_Repository(id=1, affiliation_id=1, repository_url=aff_url_1, access_token = "aaaaa")
    test_affiliation_repository_2 = Affiliation_Repository(id=2, affiliation_id=2, repository_url=aff_url_2, access_token = "bbbbb")
    # 正常系
    result = manager.create_aff_repository(test_affiliation_repository_1)
    assert (test_affiliation_repository_1.id == result.id and test_affiliation_repository_1.affiliation_id == result.affiliation_id and test_affiliation_repository_1.repository_url == result.repository_url and test_affiliation_repository_1.access_token == result.access_token)
    # 異常系
    with pytest.raises(Exception) as ex:
        result = manager.create_aff_repository("test_affiliation_repository_1")
    
    # 正常系
    aff_repository = {"id":test_affiliation_repository_1.id,
                        "affiliation_id":test_affiliation_repository_1.id,
                        "repository_url":test_affiliation_repository_1.repository_url,
                        "access_token":"ccccc"}
    result = manager.upt_aff_repository(aff_repository)
    db_result = manager.get_aff_repository_by_affiliation_id(test_affiliation_repository_1.affiliation_id)
    assert result == db_result
    
    aff_repository["id"] = 5
    result = manager.upt_aff_repository(aff_repository)
    db_result = manager.get_aff_repository_by_affiliation_id(test_affiliation_repository_1.affiliation_id)
    assert result != db_result
    
    aff_repository["id"] = 1
    aff_repository["access_token"] = "aaaaa"
    result = manager.upt_aff_repository(aff_repository)
    db_result = manager.get_aff_repository_by_affiliation_id(test_affiliation_repository_1.affiliation_id)
    assert result == db_result
    
    # 異常系
    with pytest.raises(Exception) as ex:
        result = manager.upt_aff_repository("test_affiliation_repository_1")
    
    result = manager.create_aff_repository(test_affiliation_repository_2)
    assert (test_affiliation_repository_2.id == result.id and test_affiliation_repository_2.affiliation_id == result.affiliation_id and test_affiliation_repository_2.repository_url == result.repository_url and test_affiliation_repository_2.access_token == result.access_token)
    
    result = manager.get_aff_repository_by_affiliation_id(test_affiliation_repository_1.affiliation_id)
    assert (test_affiliation_repository_1.id == result.id and test_affiliation_repository_1.affiliation_id == result.affiliation_id and test_affiliation_repository_1.repository_url == result.repository_url and test_affiliation_repository_1.access_token == result.access_token)

    assert manager.get_aff_repository_by_affiliation_id(999999) == None
    
    

    result = manager.get_aff_repository_by_affiliation_name(test_affiliation_id_1.affiliation_name)
    assert (test_affiliation_repository_1.id == result.id and test_affiliation_repository_1.affiliation_id == result.affiliation_id and test_affiliation_repository_1.repository_url == result.repository_url and test_affiliation_repository_1.access_token == result.access_token)
    
    assert manager.get_aff_repository_by_affiliation_name("Not exist") == None    
    
    result = manager.get_affiliation_repository_list()
    assert result == [test_affiliation_repository_1, test_affiliation_repository_2]
    