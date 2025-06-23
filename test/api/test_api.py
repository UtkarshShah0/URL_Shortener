
def test_create_short_url(client):
    res = client.post("/shorten", json={"original_url": "https://example.com"})
    assert res.status_code == 200
    data = res.json()
    assert "short_code" in data
    assert data["original_url"] == "https://example.com"

def test_redirect_url(client):
    post = client.post("/shorten", json={"original_url": "https://example.com"})
    short_code = post.json()["short_code"]
    redirect = client.get(f"/{short_code}", allow_redirects=False)
    assert redirect.status_code in [307, 302]

def test_info_endpoint(client):
    post = client.post("/shorten", json={"original_url": "https://example.com"})
    short_code = post.json()["short_code"]
    res = client.get(f"/info/{short_code}")
    assert res.status_code == 200
    assert res.json()["original_url"] == "https://example.com"

def test_update_endpoint(client):
    post = client.post("/shorten", json={"original_url": "https://old.com"})
    short_code = post.json()["short_code"]
    res = client.put(f"/update/{short_code}", json={"original_url": "https://new.com"})
    assert res.status_code == 200
    assert res.json()["original_url"] == "https://new.com"

def test_delete_endpoint(client):
    post = client.post("/shorten", json={"original_url": "https://to-delete.com"})
    short_code = post.json()["short_code"]
    res = client.delete(f"/delete/{short_code}")
    assert res.status_code == 200
    assert res.json()["message"] == "Deleted successfully"

def test_create_with_invalid_url(client):
    res = client.post("/shorten", json={"original_url": ""})
    assert res.status_code == 422  # Unprocessable Entity (FastAPI validation)

def test_redirect_with_invalid_code(client):
    res = client.get("/invalidcode", allow_redirects=False)
    assert res.status_code == 404
    assert res.json()["detail"] == "Not found"

def test_info_with_invalid_code(client):
    res = client.get("/info/doesnotexist")
    assert res.status_code == 404
    assert res.json()["detail"] == "Not found"

def test_update_invalid_code(client):
    res = client.put("/update/nocode", json={"original_url": "https://new.com"})
    assert res.status_code == 404
    assert res.json()["detail"] == "Short code not found"

def test_delete_invalid_code(client):
    res = client.delete("/delete/unknown")
    assert res.status_code == 404
    assert res.json()["detail"] == "Not found"
