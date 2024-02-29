from login.views import generate_random_str

def test_generate_random_str():
    assert generate_random_str()