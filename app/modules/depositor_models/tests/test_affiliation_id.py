from mock import patch,MagicMock
import pytest
from depositor_models.affiliation_id import Affiliation_Id, Affiliation_Id_manager


def test_Affiliation_Id_manager(app, db):
    manager = Affiliation_Id_manager()
    aff_idp_url_1 = "https://idp.auth.alphaalpha.ac.jp/idp/profile/SAML2/Redirect/SSO"
    aff_idp_url_2 = "https://idp.auth.betabeta.ac.jp/idp/profile/SAML2/Redirect/SSO"
    test_affiliation_id_1 = Affiliation_Id(id=1, affiliation_idp_url=aff_idp_url_1, affiliation_name="alpha")
    test_affiliation_id_2 = Affiliation_Id(id=2, affiliation_idp_url=aff_idp_url_2, affiliation_name="beta")
    # 正常系
    result = manager.create_affiliation_id(test_affiliation_id_1)
    db_result = manager.get_affiliation_id_by_id(1)
    assert (test_affiliation_id_1.id == result.id and test_affiliation_id_1.affiliation_idp_url == result.affiliation_idp_url and test_affiliation_id_1.affiliation_name == result.affiliation_name)
    assert (test_affiliation_id_1.id == db_result.id and test_affiliation_id_1.affiliation_idp_url == db_result.affiliation_idp_url and test_affiliation_id_1.affiliation_name == db_result.affiliation_name)
    # 異常系
    with pytest.raises(Exception) as ex:
        result = manager.create_affiliation_id("test_affiliation_id_1")
    
    result = manager.create_affiliation_id(test_affiliation_id_2)
    db_result = manager.get_affiliation_id_by_id(2)
    assert (test_affiliation_id_2.id == result.id and test_affiliation_id_2.affiliation_idp_url == result.affiliation_idp_url and test_affiliation_id_2.affiliation_name == result.affiliation_name)
    assert (test_affiliation_id_2.id == db_result.id and test_affiliation_id_2.affiliation_idp_url == db_result.affiliation_idp_url and test_affiliation_id_2.affiliation_name == db_result.affiliation_name)
    
    assert manager.get_affiliation_id_by_id(99999)==None
    
    result = manager.get_affiliation_id_by_affiliation_name(test_affiliation_id_1.affiliation_name)
    assert (test_affiliation_id_1.id == result.id and test_affiliation_id_1.affiliation_idp_url == result.affiliation_idp_url and test_affiliation_id_1.affiliation_name == result.affiliation_name)
    
    assert manager.get_affiliation_id_by_affiliation_name("Not exist") == None
    
    result = manager.get_affiliation_id_by_idp_url(test_affiliation_id_1.affiliation_idp_url)
    assert (test_affiliation_id_1.id == result.id and test_affiliation_id_1.affiliation_idp_url == result.affiliation_idp_url and test_affiliation_id_1.affiliation_name == result.affiliation_name)

    assert manager.get_affiliation_id_by_idp_url("Not exist") == None
    
    result = manager.get_affiliation_id_list()
    assert result == [test_affiliation_id_1, test_affiliation_id_2]
    