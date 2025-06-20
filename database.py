from sqlmodel import SQLModel, create_engine, Session, select
from models import ShortURL
from sqlalchemy.exc import IntegrityError
from typing import Optional
from datetime import datetime, timezone
import random, string


DATABASE_URL = "sqlite:///./shortener.db"
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def create_short_url(original_url: str, session: Session) -> Optional[ShortURL]:
    for _ in range(5):
        short_code = generate_short_code()
        new_url = ShortURL(
            original_url=original_url,
            short_code=short_code,
            click_count=0
        )
        session.add(new_url)
        try:
            session.commit()
            session.refresh(new_url)
            return new_url
        except IntegrityError:
            session.rollback()
    return None


def get_url_by_code(short_code: str, session: Session) -> Optional[ShortURL]:
    return session.exec(select(ShortURL).where(ShortURL.short_code == short_code)).first()


def increment_click_count(url_obj: ShortURL, session: Session):
    url_obj.click_count += 1
    session.add(url_obj)
    session.commit()


def delete_short_url(short_code: str, session: Session) -> bool:
    obj = get_url_by_code(short_code, session)
    if not obj:
        return False
    session.delete(obj)
    session.commit()
    return True


def update_short_url(short_code: str, new_url: str, session: Session) -> Optional[ShortURL]:
    url_obj = get_url_by_code(short_code, session)
    if not url_obj:
        return None
    url_obj.original_url = new_url
    session.add(url_obj)
    session.commit()
    session.refresh(url_obj)
    return url_obj