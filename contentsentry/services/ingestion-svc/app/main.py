import json
import uuid
from datetime import datetime, timezone

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .aws import upload_content, enqueue_job
from .config import settings

app = FastAPI(title="ContentSentry Ingestion Service")

class IngestRequest(BaseModel):
    url: str | None = None      # ingest by fetching a URL
    content: str | None = None  # or ingest raw text directly

@app.get("/health")
def health():
    return {"status": "ok", "service": "ingestion-svc"}

@app.post("/ingest")
def ingest(req: IngestRequest):
    if not req.url and not req.content:
        raise HTTPException(
            status_code=400,
            detail="Provide either 'url' or 'content'.",
        )

    # 1. Get the content (fetch URL or use provided text)
    if req.url:
        try:
            resp = httpx.get(req.url, timeout=10.0, follow_redirects=True)
            resp.raise_for_status()
            body = resp.text.encode("utf-8")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch URL: {e}",
            )
    else:
        body = req.content.encode("utf-8")

    # 2. Generate a unique run_id and S3 key
    run_id = str(uuid.uuid4())
    s3_key = f"raw/{run_id}.html"

    # 3. Store the raw content in S3
    upload_content(s3_key, body)

    # 4. Build a job message and push to SQS
    job = {
        "run_id": run_id,
        "s3_bucket": settings.raw_content_bucket,
        "s3_key": s3_key,
        "source_url": req.url,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }
    enqueue_job(json.dumps(job))

    # 5. Return the run_id so the caller can track it
    return {
        "run_id": run_id,
        "status": "queued",
        "s3_key": s3_key,
    }