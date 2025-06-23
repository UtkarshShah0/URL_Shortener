from database import generate_short_code, init_db, create_short_url, get_session, get_url_by_code
from sqlmodel import Session
from models import ShortURL
import database
from database import increment_click_count, delete_short_url, create_short_url, update_short_url


def test_generate_short_code_length():
    code = generate_short_code()
    assert len(code) == 6

def test_generate_short_code_uniqueness():
    codes = {generate_short_code() for _ in range(100)}
    assert len(codes) == 100

def test_init_db_does_not_crash():
    init_db()

def test_create_short_url_success(client):
    with next(get_session()) as session:
        result = create_short_url("https://test.com", session)
        assert result is not None
        assert result.original_url == "https://test.com"
        assert isinstance(result.short_code, str)

def test_create_short_url_collision(client):
    with next(get_session()) as session:
        short_code = "abc123"
        session.add(ShortURL(original_url="https://x.com", short_code=short_code, click_count=0))
        session.commit()

        database.generate_short_code = lambda: short_code

        result = create_short_url("https://y.com", session)
        assert result is None  

def test_get_url_by_code(client):
    with next(get_session()) as session:
        created = create_short_url("https://a.com", session)
        found = get_url_by_code(created.short_code, session)
        assert found is not None
        assert found.original_url == "https://a.com"

def test_increment_click_count(client):
    with next(get_session()) as session:
        from database import create_short_url
        url = create_short_url("https://click.com", session)
        old_count = url.click_count
        increment_click_count(url, session)
        assert url.click_count == old_count + 1

def test_delete_short_url_success(client):
    with next(get_session()) as session:
        url = create_short_url("https://del.com", session)
        result = delete_short_url(url.short_code, session)
        assert result is True

def test_delete_short_url_fail(client):
    with next(get_session()) as session:
        result = delete_short_url("notfound", session)
        assert result is False

def test_update_short_url_success(client):
    with next(get_session()) as session:
        url = create_short_url("https://old.com", session)
        updated = update_short_url(url.short_code, "https://new.com", session)
        assert updated.original_url == "https://new.com"

def test_update_short_url_fail(client):
    with next(get_session()) as session:
        updated = update_short_url("invalid", "https://x.com", session)
        assert updated is None