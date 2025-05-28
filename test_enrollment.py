import pytest
from application import app
from application.extensions import db
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['MONGODB_SETTINGS'] = {'db': 'testdb', 'host': 'mongomock://localhost'}
    client = app.test_client()

    # Reset the database before tests
    with app.app_context():
        db.connection.drop_database('testdb')

    yield client


def test_create_enrollment(client):
    response = client.post('/api/enrollments', json={
        'user_id': 1,
        'courseID': 'CS101'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['user_id'] == 1
    assert data['courseID'] == 'CS101'


def test_get_all_enrollments(client):
    client.post('/api/enrollments', json={'user_id': 2, 'courseID': 'CS102'})
    response = client.get('/api/enrollments')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(e['courseID'] == 'CS102' for e in data)


def test_update_enrollment(client):
    client.post('/api/enrollments', json={'user_id': 3, 'courseID': 'CS103'})
    get_response = client.get('/api/enrollments')
    enrollment_list = get_response.get_json()
    target = next((e for e in enrollment_list if e['courseID'] == 'CS103'), None)
    assert target is not None

    enrollment_id = target.get('id') or target.get('_id')
    assert enrollment_id is not None, "No 'id' or '_id' field in enrollment"

    response = client.put(f"/api/enrollments/{enrollment_id}", json={'courseID': 'CS104'})
    assert response.status_code in [200, 204]

def test_delete_enrollment(client):
    client.post('/api/enrollments', json={'user_id': 4, 'courseID': 'CS105'})
    get_response = client.get('/api/enrollments')
    enrollment_list = get_response.get_json()
    target = next((e for e in enrollment_list if e['courseID'] == 'CS105'), None)
    assert target is not None

    enrollment_id = target.get('id') or target.get('_id')
    assert enrollment_id is not None, "No 'id' or '_id' field in enrollment"

    response = client.delete(f"/api/enrollments/{enrollment_id}")
    assert response.status_code in [200, 204]


def test_get_invalid_enrollment(client):
    response = client.get('/api/enrollments/invalid_id')
    assert response.status_code in [400, 404]


def test_update_invalid_enrollment(client):
    response = client.put('/api/enrollments/invalid_id', json={'courseID': 'FAIL'})
    assert response.status_code in [400, 404]


def test_delete_invalid_enrollment(client):
    response = client.delete('/api/enrollments/invalid_id')
    assert response.status_code in [400, 404]
