from app.app import get_hash, verify_hash
import re
import pytest
import sqlite3


def test_get_hash():
    assert get_hash("hello") != "hello"
    assert get_hash("strive") != "strive"


def test_bcrypt():

    bcrypt_hash_pattern = r"^\$2[ayb]\$.{56}$"
    pat = re.compile(bcrypt_hash_pattern)

    new_hash = get_hash("Hello")

    assert pat.search(new_hash)


@pytest.mark.parametrize("testing_string", [("hello"), ("strive"), ("asdasd")])
def test_hash_computation(testing_string):
    # testing_string = "hello"
    new_hash = get_hash(testing_string)

    assert verify_hash(testing_string, new_hash)


@pytest.mark.parametrize(
    "email,password", [("hello@hello.com", "asd"),
                       ("strive@strive.com", "asdasd")]
)
def test_user_creation(email, password):
    # 1. verify user is created
    conn = sqlite3.connect("app/ml_app.db", check_same_thread=False)
    with conn as c:
        assert c.execute(
            "SELECT * FROM users WHERE email = ? and password = ?", (email, get_hash(password)))
    # 2. verify you can validate the hash
