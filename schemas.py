from pydantic import BaseModel
from datetime import datetime


class URLCreate(BaseModel):
    original_url: str

class URLUpdate(BaseModel):
    original_url: str

class URLInfo(BaseModel):
    id: int
    original_url: str
    short_code: str
    created_at: datetime
    click_count: int

    class Config:
        from_attributes = True