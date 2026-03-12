def test_signup_adds_new_participant(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/signup"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(endpoint, params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"
    assert email in participants


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown%20Club/signup"
    email = "student@mergington.edu"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_registration(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/signup"
    email = "michael@mergington.edu"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_increases_participant_count_by_one(client):
    # Arrange
    before = client.get("/activities").json()["Programming Class"]["participants"]
    before_count = len(before)
    endpoint = "/activities/Programming%20Class/signup"
    email = "countcheck@mergington.edu"

    # Act
    response = client.post(endpoint, params={"email": email})
    after = client.get("/activities").json()["Programming Class"]["participants"]

    # Assert
    assert response.status_code == 200
    assert len(after) == before_count + 1
