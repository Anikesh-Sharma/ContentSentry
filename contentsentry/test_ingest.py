import httpx

resp = httpx.post(
    "http://localhost:8000/ingest",
    json={"url": "https://www.google.com"},
    timeout=60.0,
)
print(resp.json())