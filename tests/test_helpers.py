# tests/test_helpers.py in learning-path-service
import re
import uuid
from datetime import datetime
import types
import pytest
import builtins
from app import helpers



# --- gen_id ---
def test_gen_id_prefix_and_valid_uuid():
    value = helpers.gen_id("lp")
    # Muss mit Prefix starten
    assert value.startswith("lp-")
    # Regex-Struktur prüfen (UUID hat 36 Zeichen inkl. Bindestriche)
    assert re.match(r"^lp-[0-9a-fA-F-]{36}$", value)
    # UUID-Teil extrahieren und wirklich als UUID validieren
    uuid_part = value.split("-", 1)[1]
    uuid.UUID(uuid_part)


def test_gen_id_ids_unique():
    prefix = "lp"
    value1 = helpers.gen_id(prefix)
    value2 = helpers.gen_id(prefix)
    assert value1 != value2



# --- now_dt ---
def test_now_dt_returns_datetime():
    date = helpers.now_dt()
    assert isinstance(date, datetime)



# --- get_json ---

# --- get_json: Hilfsfunktion zum Patchen ---
class _MockResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self._status_code = status_code

    def json(self):
        return self._payload
    
    def raise_for_status(self):
        if not (200 <= self._status_code < 300):
            raise Exception("HTTP error")
    

def test_get_json_returns_plain_payload(monkeypatch):
    def mock_get(url, timeout=10):
        return _MockResponse([{"id": "a"}, {"id": "b"}])
    
    monkeypatch.setattr(helpers.requests, "get", mock_get)

    response = helpers.get_json("http://example/api")
    assert response == [{"id": "a"}, {"id": "b"}]


def test_get_json_unwrap_data_array(monkeypatch):
    def mock_get(url, timeout=10):
        return _MockResponse({"data": [{"id": 1}, {"id": 2}]})
    
    monkeypatch.setattr(helpers.requests, "get", mock_get)

    response = helpers.get_json("http://fake/api")
    assert response == [{"id": 1}, {"id": 2}]
