from mock import patch,MagicMock
import pytest
from depositor_models.user import User, User_manager


def test_User_manager(app, db):
    manager = User_manager()
    test_user_1 = User(id=1, user_id="test_user@test.com", affiliation_id=1, user_orcid = "test_user", role = "")
    test_user_2 =User(id=2, user_id="TEST_USER@test.com", affiliation_id=1, user_orcid = "test_user", role = "Admin")
    # 正常系
    result = manager.create_user(test_user_1)
    db_result = manager.get_user_by_id(1)
    assert (test_user_1.id == result.id and test_user_1.user_id == result.user_id and test_user_1.affiliation_id == result.affiliation_id and test_user_1.user_orcid == result.user_orcid)
    assert (test_user_1.id == db_result.id and test_user_1.user_id == db_result.user_id and test_user_1.affiliation_id == db_result.affiliation_id and test_user_1.user_orcid == db_result.user_orcid)
    # 異常系
    with pytest.raises(Exception) as ex:
        # test_user_1 =User(id="あああ", user_id="test_user@test.com", affiliation_id=1, user_orcid = "test_user", role = "")
        result = manager.create_user("test_user_1")
    
    result = manager.create_user(test_user_2)
    db_result = manager.get_user_by_id(2)
    assert (test_user_2.id == result.id and test_user_2.user_id == result.user_id and test_user_2.affiliation_id == result.affiliation_id and test_user_2.user_orcid == result.user_orcid)
    assert (test_user_2.id == db_result.id and test_user_2.user_id == db_result.user_id and test_user_2.affiliation_id == db_result.affiliation_id and test_user_2.user_orcid == db_result.user_orcid)
    
    assert manager.get_user_by_id(999999) == None
    
    result = manager.get_user_by_user_id(test_user_1.user_id)
    assert (test_user_1.id == result.id and test_user_1.user_id == result.user_id and test_user_1.affiliation_id == result.affiliation_id and test_user_1.user_orcid == result.user_orcid)

    assert manager.get_user_by_user_id("Not exist") == None
    
    result = manager.get_users_by_affiliation_id(1)
    assert result == [test_user_1,test_user_2]
    
    assert manager.get_users_by_affiliation_id(9999999) == []   