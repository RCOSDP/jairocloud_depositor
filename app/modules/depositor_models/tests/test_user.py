from depositor_models.user import User, User_manager


def test_User_manager(app, db):
    manager = User_manager()
    test_user = User(id=10, user_id="test_user@test.com", affiliation_id=1, user_orcid = "test_user", role = "")
    manager.create_user(test_user)
    result = manager.get_user_by_id(10)
    assert test_user == result
    