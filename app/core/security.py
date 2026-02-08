import hmac
import hashlib
from fastapi import Request, HTTPException
from .config import META_APP_SECRET

def verify_meta_signature(request: Request, body: bytes):
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        raise HTTPException(status_code=401, detail="Missing signature")

    expected = (
        "sha256="
        + hmac.new(
            META_APP_SECRET.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
    )

    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=401, detail="Invalid signature")
