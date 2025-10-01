# tests/test_clients.py in learning-path-service
import pytest
from app import clients

# Hilfsklasse, um aufgerufene URLs zu prüfen
class _Capture:
    def __init__(self):
        self.calls = []


def test_fetch_topics(monkeypatch):
    cap = _Capture()

    def fake_get_json(url, timeout=10):
        cap.calls.append(url)
        return [{"id": "t1", "name": "Topic 1"}]

    monkeypatch.setattr(clients, "get_json", fake_get_json)

    response = clients.fetch_topics()

    assert response == [{"id": "t1", "name": "Topic 1"}]
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/topics")


def test_fetch_skills(monkeypatch):
    cap = _Capture()

    def fake_get_json(url, timeout=10):
        cap.calls.append(url)
        return [{"id": "s1", "name": "Skill 1"}]

    monkeypatch.setattr(clients, "get_json", fake_get_json)

    response = clients.fetch_skills()

    assert response == [{"id": "s1", "name": "Skill 1"}]
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/skills")


def test_fetch_resources(monkeypatch):
    cap = _Capture()

    fake_items = [{"_id": "r1", "title": "Resource 1"}]

    def fake_get_json(url, timeout=10):
        cap.calls.append(url)
        return fake_items

    monkeypatch.setattr(clients, "get_json", fake_get_json)

    response = clients.fetch_resources()

    expected = [{"_id": "r1", "title": "Resource 1", "id": "r1"}]

    assert response == expected
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/resources")