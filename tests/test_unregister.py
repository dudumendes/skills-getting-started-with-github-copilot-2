def test_unregister_removes_existing_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "michael@mergington.edu" not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Club/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_registered_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "notregistered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_decreases_participant_count_by_one(client):
    before = client.get("/activities").json()["Soccer Club"]["participants"]
    before_count = len(before)

    response = client.delete(
        "/activities/Soccer%20Club/participants",
        params={"email": "alex@mergington.edu"},
    )

    after = client.get("/activities").json()["Soccer Club"]["participants"]

    assert response.status_code == 200
    assert len(after) == before_count - 1
