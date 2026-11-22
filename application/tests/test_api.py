
def sample_employee():
    return {
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "department": "Engineering",
        "designation": "Software Engineer"
    }


def test_health_check(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_add_employee(client):
    response = client.post(
        "/api/employees",
        json=sample_employee()
    )

    assert response.status_code == 201
    assert response.json["employee"]["name"] == "Rahul Sharma"


def test_get_employees(client):
    client.post("/api/employees", json=sample_employee())

    response = client.get("/api/employees")

    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_single_employee(client):
    create_response = client.post(
        "/api/employees",
        json=sample_employee()
    )

    employee_id = create_response.json["employee"]["id"]

    response = client.get(
        f"/api/employees/{employee_id}"
    )

    assert response.status_code == 200
    assert response.json["email"] == "rahul@example.com"


def test_update_employee(client):
    create_response = client.post(
        "/api/employees",
        json=sample_employee()
    )

    employee_id = create_response.json["employee"]["id"]

    updated_data = sample_employee()
    updated_data["name"] = "Rahul Updated"

    response = client.put(
        f"/api/employees/{employee_id}",
        json=updated_data
    )

    assert response.status_code == 200
    assert response.json["employee"]["name"] == "Rahul Updated"


def test_delete_employee(client):
    create_response = client.post(
        "/api/employees",
        json=sample_employee()
    )

    employee_id = create_response.json["employee"]["id"]

    response = client.delete(
        f"/api/employees/{employee_id}"
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/employees/{employee_id}"
    )

    assert get_response.status_code == 404


def test_duplicate_email(client):
    client.post("/api/employees", json=sample_employee())

    response = client.post(
        "/api/employees",
        json=sample_employee()
    )

    assert response.status_code == 409


def test_missing_employee_fields(client):
    response = client.post(
        "/api/employees",
        json={"name": "Rahul Sharma"}
    )

    assert response.status_code == 400
