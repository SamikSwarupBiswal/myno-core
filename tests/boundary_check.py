"""
Phase 1.1 Boundary Tests — MYNO
Purpose:
Freeze behavior gating invariants.
If ANY of these fail, Phase 1.1 is NOT locked.
"""

import json
import copy
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ─────────────────────────────
# Helpers
# ─────────────────────────────

VALID_MESSAGE_PAYLOAD = {
    "entry": [
        {
            "changes": [
                {
                    "value": {
                        "messages": [
                            {
                                "id": "wamid.TEST_MESSAGE_ID",
                                "from": "911234567890",
                                "type": "text",
                                "text": {"body": "Hi"}
                            }
                        ]
                    }
                }
            ]
        }
    ]
}

VALID_HEADERS = {
    # NOTE: Signature verification is bypassed in tests
    # If you enable strict signature checks, mock this
    "X-Hub-Signature-256": "sha256=test"
}


def post(payload):
    return client.post(
        "/webhook",
        headers=VALID_HEADERS,
        data=json.dumps(payload)
    )


# ─────────────────────────────
# TESTS
# ─────────────────────────────

def test_single_message_gets_single_reply():
    """One message → one OK"""
    response = post(VALID_MESSAGE_PAYLOAD)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_duplicate_message_id_is_ignored():
    """Same message retried → ignored"""
    post(VALID_MESSAGE_PAYLOAD)
    response = post(VALID_MESSAGE_PAYLOAD)
    assert response.status_code == 200
    assert response.json()["status"] == "duplicate_ignored"


def test_status_event_does_not_trigger_reply():
    """Delivery/read receipts must be silent"""
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "statuses": [
                                {"status": "delivered"}
                            ]
                        }
                    }
                ]
            }
        ]
    }
    response = post(payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ignored_non_message"


def test_non_text_message_is_ignored():
    """Images, audio, etc. must not trigger replies"""
    payload = copy.deepcopy(VALID_MESSAGE_PAYLOAD)
    payload["entry"][0]["changes"][0]["value"]["messages"][0]["type"] = "image"
    payload["entry"][0]["changes"][0]["value"]["messages"][0].pop("text", None)

    response = post(payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ignored_non_text"


def test_malformed_payload_does_not_crash():
    """Garbage input → 200 OK"""
    response = client.post("/webhook", json={"foo": "bar"})
    assert response.status_code == 200


def test_missing_message_id_is_ignored():
    """No message ID → no reply"""
    payload = copy.deepcopy(VALID_MESSAGE_PAYLOAD)
    payload["entry"][0]["changes"][0]["value"]["messages"][0].pop("id")

    response = post(payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ignored_no_message_id"


def test_invalid_signature_rejected(monkeypatch):
    """Invalid signature must hard-fail in production mode"""
    monkeypatch.delenv("MYNO_TEST_MODE", raising=False)

    response = client.post(
        "/webhook",
        headers={"X-Hub-Signature-256": "sha256=invalid"},
        data=json.dumps(VALID_MESSAGE_PAYLOAD)
    )
    assert response.status_code == 401

