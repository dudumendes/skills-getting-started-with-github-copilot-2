def test_root_redirects_to_static_index(client):
    # Arrange
    endpoint = "/"

    # Act
    response = client.get(endpoint, follow_redirects=False)

    # Assert
    assert response.status_code in (307, 302)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_seeded_activities(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert len(payload) == 9
    assert "Chess Club" in payload


def test_get_activities_includes_expected_fields_for_each_activity(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    for details in payload.values():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)


def test_get_activities_sets_no_store_cache_header(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"


def test_get_activities_contains_seed_participants(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert "michael@mergington.edu" in payload["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in payload["Chess Club"]["participants"]
