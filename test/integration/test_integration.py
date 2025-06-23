from database import create_short_url, get_url_by_code, delete_short_url
from sqlmodel import Session
from models import ShortURL
from test.conftest import override_get_session

def test_create_and_retrieve(session: Session = next(override_get_session())):
    url = create_short_url("https://example.com", session)
    fetched = get_url_by_code(url.short_code, session)
    assert fetched.original_url == "https://example.com"

def test_delete_url(session: Session = next(override_get_session())):
    url = create_short_url("https://example.com", session)
    assert delete_short_url(url.short_code, session) is True
