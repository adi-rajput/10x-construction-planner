# tests/test_api.py
from fastapi.testclient import TestClient
from backend.main import app
import time

client = TestClient(app)

def test_create_and_get_and_delete():
    payload = {
        "name":"test1",
        "wall":{"width":5,"height":5},
        "obstacles":[{"x":1,"y":1,"width":0.25,"height":0.25}],
        "resolution":0.2
    }
    t0 = time.time()
    r = client.post("/trajectory/create", json=payload)
    assert r.status_code == 200
    res = r.json()
    duration = res.get("duration_ms", None)
    assert duration is not None
    tid = res["id"]

    r2 = client.get(f"/trajectory/{tid}")
    assert r2.status_code == 200
    obj = r2.json()
    assert obj["name"] == "test1"
    assert isinstance(obj["path"], list)
    assert obj["meta"]["wall"]["width"] == 5

    # delete
    r3 = client.delete(f"/trajectory/{tid}")
    assert r3.status_code == 200
