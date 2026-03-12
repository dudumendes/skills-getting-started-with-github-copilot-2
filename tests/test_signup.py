def test_signup_adds_new_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "newstudent@mergington.edu" in participants


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_registration(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_increases_participant_count_by_one(client):
    before = client.get("/activities").json()["Programming Class"]["participants"]
    before_count = len(before)

    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": "countcheck@mergington.edu"},
    )

    after = client.get("/activities").json()["Programming Class"]["participants"]

    assert response.status_code == 200
    assert len(after) == before_count + 1
