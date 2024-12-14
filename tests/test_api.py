import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to StressMinder API"}


def test_create_sensor_reading():
    """Test sensor data creation"""
    sensor_data = {
        "temperatura": 36.5,
        "ritmo_cardiaco": 85,
        "indice_facial": 0.75,  # Optional field
    }
    response = client.post("/api/v1/sensors/", json=sensor_data)
    assert response.status_code == 201
    data = response.json()
    assert data["temperatura"] == sensor_data["temperatura"]
    assert data["ritmo_cardiaco"] == sensor_data["ritmo_cardiaco"]
    assert data["indice_facial"] == sensor_data["indice_facial"]
    assert "id" in data
    assert "timestamp" in data


def test_get_latest_readings():
    """Test getting latest sensor readings"""
    response = client.get("/api/v1/sensors/latest")
    assert response.status_code in [200, 404]  # 404 if no readings yet
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            reading = data[0]
            assert "temperatura" in reading
            assert "ritmo_cardiaco" in reading
            assert "indice_facial" in reading
            assert "timestamp" in reading


@pytest.mark.skip(reason="Table question_responses not created yet")
def test_submit_question():
    """Test question submission"""
    question_data = {"question_number": 1, "answer_value": 2}
    response = client.post("/api/v1/questions/", json=question_data)
    assert response.status_code == 200
    data = response.json()
    assert data["question_number"] == question_data["question_number"]
    assert data["answer_value"] == question_data["answer_value"]


@pytest.mark.skip(reason="Table question_responses not created yet")
def test_get_pss10_result():
    """Test getting PSS-10 results"""
    response = client.get("/api/v1/questions/pss10")
    assert response.status_code in [200, 404]  # 404 if not enough responses
    if response.status_code == 200:
        data = response.json()
        assert "total_score" in data
        assert "stress_level" in data
        assert "timestamp" in data


@pytest.mark.skip(reason="Table question_responses not created yet")
def test_get_stress_analysis():
    """Test getting stress analysis"""
    response = client.get("/api/v1/results/")
    assert response.status_code in [200, 404]  # 404 if no data yet
    if response.status_code == 200:
        data = response.json()
        assert "timestamp" in data
        assert "total_stress_index" in data
        assert 0 <= data["total_stress_index"] <= 1
        assert isinstance(data["partial_indices"], list)
