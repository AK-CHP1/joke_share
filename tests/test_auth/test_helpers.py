from joke_share.auth.helpers import *


def test_is_valid_username():
    assert is_valid_username("223aayush")
    assert is_valid_username("ccasfd_33")
    assert is_valid_username("_323asfsdf")
    assert is_valid_username("ccdd-weww")

    assert not is_valid_username("@erwe11")
    assert not is_valid_username("34=asfss")
    assert not is_valid_username("...234adsf@@!")


def test_is_valid_email():
    assert is_valid_email("myemail@email.com")
    assert is_valid_email("a_validemail_233@email.com")
    assert is_valid_email("__email.231aa-ccdd@email.co.in")

    assert not is_valid_email("an^invalid^email@454.com")
    assert not is_valid_email("yet another invalid email@email.com")
    assert not is_valid_email("adfewss..wew4*asdf@co.do.in")


def test_is_valid_password():
    assert is_valid_passowrd("fasdfuiAA90*")
    assert is_valid_passowrd("_fasdfu  iAA90*")
    assert is_valid_passowrd("_Pass90_")

    assert not is_valid_passowrd("mypass")
    assert not is_valid_passowrd("Password90")
    assert not is_valid_passowrd("myPassword")
    assert not is_valid_passowrd("_mypass90_")