def test_unregister_removes_existing_participant(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/participants"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown%20Club/participants"
    email = "student@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_registered_participant(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/participants"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_decreases_participant_count_by_one(client):
    # Arrange
    before = client.get("/activities").json()["Soccer Club"]["participants"]
    before_count = len(before)
    endpoint = "/activities/Soccer%20Club/participants"
    email = "alex@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})
    after = client.get("/activities").json()["Soccer Club"]["participants"]

    # Assert
    assert response.status_code == 200
    assert len(after) == before_count - 1
