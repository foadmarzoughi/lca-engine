"""Regression tests for the rejected-candidate guard in send_candidate_email."""

import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ["LANGSMITH_TRACING"] = "false"

from recruiting_agent.recruiting_agent import send_candidate_email

REJECTED_ID = "CAND-50003"
ALLOWED_ID = "CAND-12853"


def _send(candidate_id, candidate):
    return send_candidate_email.invoke({
        "candidate_id": candidate_id,
        "candidate": candidate,
        "subject": "Hiring manager chat",
        "body": "Are you available next week?",
        "from_recruiter": {"name": "Sara Brown", "email": "sara.brown@northpoint.com"},
    })


def test_rejected_candidate_id_is_blocked():
    result = _send(REJECTED_ID, {"name": "Sofia Rossi", "email": "sofia.rossi@example.com"})
    assert result["status"] == "blocked"
    assert result["reason"] == "candidate_rejected"
    assert "message_id" not in result


def test_missing_candidate_id_is_blocked():
    result = _send("", {"name": "Sofia Rossi", "email": "sofia.rossi@example.com"})
    assert result["status"] == "blocked"
    assert result["reason"] == "candidate_unverified"
    assert "message_id" not in result


def test_unknown_candidate_id_is_blocked():
    result = _send("CAND-5003", {"name": "Sofia Rossi", "email": "sofia.rossi@example.com"})
    assert result["status"] == "blocked"
    assert result["reason"] == "candidate_unverified"
    assert "message_id" not in result


def test_allowed_candidate_is_sent():
    result = _send(ALLOWED_ID, {"name": "Omar Okafor", "email": "omar.okafor@example.com"})
    assert result["status"] == "sent"
    assert result["message_id"]
