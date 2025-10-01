# tests/test_api_integration.py
import pytest

def _assert_ok(response, expected_status=200):
    assert response.status_code == expected_status, response.text


def test_healthz(client):
    response = client.get("/healthz")
    _assert_ok(response, 200)
    data = response.json()
    assert data.get("status") == "ok"
    assert data.get("db") == "up"


def test_generate_then_list_and_detail(client):
    # Payload für die Pfaderstellung
    payload = {
        "userId": "u-42",
        "desiredSkills": ["React"],
        "desiredTopics": ["Testing"]
    }

    # 1️⃣ POST /generate
    response = client.post("/generate", json=payload)
    _assert_ok(response, 200)
    created = response.json()

    # Prüfen, dass Path korrekt erstellt wurde
    assert "pathId" in created and created["pathId"]
    assert created.get("userId") == payload["userId"]
    assert created.get("goals") == {
        "skills": payload["desiredSkills"],
        "topics": payload["desiredTopics"]
    }
    assert isinstance(created.get("milestones"), list)

    # Erwartete Milestones aus dem Mock
    expected_milestones = [
        {
            "milestoneId": "m1",
            "type": "skill",
            "label": "Fundamentals",
            "skillId": "s-basics",
            "topicId": None,
            "resources": [{"resourceId": "r-1", "why": "Start here"}],
            "status": "pending",
        },
        {
            "milestoneId": "m2",
            "type": "topic",
            "label": "Practice React",
            "skillId": None,
            "topicId": "t-react",
            "resources": [{"resourceId": "r-2", "why": "Apply concepts"}],
            "status": "pending",
        },
    ]
    assert created.get("milestones") == expected_milestones

    response = client.get("/paths")
    _assert_ok(response, 200)
    items = response.json()
    assert isinstance(items, list)
    assert any(p["pathId"] == created["pathId"] for p in items)

    path_id = created["pathId"]
    response = client.get(f"/paths/{path_id}")
    _assert_ok(response, 200)
    detail = response.json()
    assert detail["pathId"] == path_id
    assert detail["userId"] == payload["userId"]
    assert detail["goals"] == {"skills": payload["desiredSkills"], "topics": payload["desiredTopics"]}
    assert detail["milestones"] == expected_milestones

