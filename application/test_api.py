# tests/test_api.py

import json
from __init__ import app, db
from models import Course

def setup_module(module):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()

def teardown_module(module):
    with app.app_context():
        db.drop_all()

def test_create_course():
    client = app.test_client()
    response = client.post('/api/courses', json={
        'name': 'Python 101',
        'description': 'Learn basic Python'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Python 101'

def test_get_all_courses():
    client = app.test_client()
    response = client.get('/api/courses')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_get_single_course():
    client = app.test_client()
    # First, create a course
    response = client.post('/api/courses', json={'name': 'Flask', 'description': 'Flask course'})
    course_id = response.get_json()['id']
    # Now, fetch it
    response = client.get(f'/api/courses/{course_id}')
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Flask'

def test_update_course():
    client = app.test_client()
    response = client.post('/api/courses', json={'name': 'Old Name'})
    course_id = response.get_json()['id']
    # Update
    response = client.put(f'/api/courses/{course_id}', json={'name': 'New Name'})
    assert response.status_code == 200
    assert response.get_json()['name'] == 'New Name'

def test_delete_course():
    client = app.test_client()
    response = client.post('/api/courses', json={'name': 'To Delete'})
    course_id = response.get_json()['id']
    # Delete
    response = client.delete(f'/api/courses/{course_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Course deleted'

def test_get_nonexistent_course():
    client = app.test_client()
    response = client.get('/api/courses/9999')
    assert response.status_code == 404

def test_create_course_invalid_data():
    client = app.test_client()
    response = client.post('/api/courses', json={})  # missing name
    assert response.status_code == 400
