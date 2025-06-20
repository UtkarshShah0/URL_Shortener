from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime, timezone

class ShortURL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    original_url: str
    short_code: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    click_count: int
