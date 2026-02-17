from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # basic expected keys
    assert "Basketball Club" in data

def test_signup_and_duplicate_rejected():
    activity = "Science Club"
    email = "test_student@mergington.edu"

    # ensure not already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # duplicate should be rejected
    dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup.status_code == 400
    assert dup.json()["detail"] == "Student is already signed up"

    # cleanup
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

def test_unregister_participant():
    activity = "Chess Club"
    email = "temp_remove@mergington.edu"

    # ensure present
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    resp = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]

    # deleting non-existent should return 400
    resp2 = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400
    assert resp2.json()["detail"] == "Student is not signed up"
