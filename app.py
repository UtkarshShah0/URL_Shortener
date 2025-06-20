from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse

from database import (
    get_session,
    init_db,
    create_short_url,
    get_url_by_code,
    increment_click_count,
    delete_short_url,
    update_short_url
)

from schemas import URLCreate, URLInfo, URLUpdate
from sqlmodel import Session

app = FastAPI()

init_db()

@app.get("/check")
def check():
    return {"message": "Working Alright"}


@app.post("/shorten", response_model=URLInfo)
def shorten(payload: URLCreate, session: Session = Depends(get_session)):
    result = create_short_url(payload.original_url, session)
    if not result:
        raise HTTPException(status_code=500, detail="Short code generation failed")
    return result


@app.get("/{short_code}")
def redirect(short_code: str, session: Session = Depends(get_session)):
    url = get_url_by_code(short_code, session)
    if not url:
        raise HTTPException(status_code=404, detail="Not found")
    increment_click_count(url, session)
    return RedirectResponse(url.original_url)


@app.get("/info/{short_code}", response_model=URLInfo)
def info(short_code: str, session: Session = Depends(get_session)):
    url = get_url_by_code(short_code, session)
    if not url:
        raise HTTPException(status_code=404, detail="Not found")
    return url


@app.delete("/delete/{short_code}")
def delete(short_code: str, session: Session = Depends(get_session)):
    if not delete_short_url(short_code, session):
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Deleted successfully"}


@app.put("/update/{short_code}", response_model=URLInfo)
def update(short_code: str, payload: URLUpdate, session: Session = Depends(get_session)):
    updated = update_short_url(short_code, payload.original_url, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Short code not found")
    return updated