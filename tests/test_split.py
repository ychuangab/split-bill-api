import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_three_people_split():
    """5.1 三人分帳：Alice 120, Bob 80, Carol 100"""
    resp = client.post("/split", json={
        "currency": "TWD",
        "participants": [
            {"name": "Alice", "paid": 120},
            {"name": "Bob", "paid": 80},
            {"name": "Carol", "paid": 100},
        ]
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 300.0
    assert data["per_person_share"] == 100.0

    balances = {b["name"]: b["balance"] for b in data["balances"]}
    assert balances["Alice"] == 20.0
    assert balances["Bob"] == -20.0
    assert balances["Carol"] == 0.0

    assert len(data["settlements"]) == 1
    s = data["settlements"][0]
    assert s["from"] == "Bob"
    assert s["to"] == "Alice"
    assert s["amount"] == 20.0


def test_uneven_split_with_zero_paid():
    """5.2 有人未付款：阿明 0, 小美 250, 大華 130"""
    resp = client.post("/split", json={
        "currency": "TWD",
        "participants": [
            {"name": "阿明", "paid": 0},
            {"name": "小美", "paid": 250},
            {"name": "大華", "paid": 130},
        ]
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 380.0
    assert abs(data["per_person_share"] - 126.67) < 0.01

    balances = {b["name"]: b["balance"] for b in data["balances"]}
    assert balances["阿明"] < 0
    assert balances["小美"] > 0

    # 阿明需要轉帳給小美和大華
    froms = [s["from"] for s in data["settlements"]]
    assert all(f == "阿明" for f in froms)
    total_transferred = sum(s["amount"] for s in data["settlements"])
    assert abs(total_transferred - abs(balances["阿明"])) < 0.02


def test_equal_split():
    """5.3 所有人金額相同 → settlements 為空"""
    resp = client.post("/split", json={
        "participants": [
            {"name": "A", "paid": 100},
            {"name": "B", "paid": 100},
            {"name": "C", "paid": 100},
        ]
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["settlements"] == []
    for b in data["balances"]:
        assert b["balance"] == 0.0


def test_missing_participants():
    """5.4a 缺少 participants 欄位 → 422"""
    resp = client.post("/split", json={"currency": "TWD"})
    assert resp.status_code == 422


def test_empty_participants():
    """5.4b participants 為空陣列 → 422"""
    resp = client.post("/split", json={"participants": []})
    assert resp.status_code == 422


def test_negative_paid():
    """5.4c paid 為負數 → 422"""
    resp = client.post("/split", json={
        "participants": [
            {"name": "Alice", "paid": -50},
            {"name": "Bob", "paid": 100},
        ]
    })
    assert resp.status_code == 422
