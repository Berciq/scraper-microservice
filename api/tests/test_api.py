import pytest

from api.config import db

def test_swagger_ui_enabled(client):
    swagger_ui = client.get('/')
    assert swagger_ui.status_code == 200
    assert b"Swagger UI" in swagger_ui.data

@pytest.mark.parametrize(
    "data, expected_status, expected_data",
    [
        (
            {"url": "http://www.example.com"},
            201,
            {},
        ),
        (
            {"url": "http://www.example.com#fragment"},
            201,
            {"url": "http://www.example.com"},
        ),
        (
            {"url": "http://www.example.com", "scrape_text": False, "scrape_images": True},
            201,
            {"scrape_text": False, "scrape_images": True},
        ),
        (
            {"url": "http://www.example.com", "scrape_text": True, "scrape_images": False},
            201,
            {"scrape_text": True, "scrape_images": False},
        ),
        (
            {"url": "http://www.example.com", "scrape_text": False, "scrape_images": False},
            400,
            {},
        ),
        (
            {"url": "not.a.url"},
            400,
            {},
        ),
    ]
)
def test_create_job(client, data, expected_status, expected_data):
    response = client.post('/scrape-jobs', json=data)
    assert response.status_code == expected_status
    if response.status_code == 200:
        assert all(item in response.json.items() for item in expected_data.items())

@pytest.mark.parametrize(
    "data1, data2, expected_status2, expected_data2",
    [
        (
            {"url": "http://www.example.com"},
            {"url": "http://www.example.com"},
            303,
            {},
        ),
        (
            {"url": "http://www.example.com"},
            {"url": "http://www.example.com#fragment"},
            303,
            {},
        ),
        (
            {"url": "http://www.example.com"},
            {"url": "http://www.example.com?v=2"},
            201,
            {},
        ),
        (
            {"url": "http://www.example.com"},
            {"url": "http://www.example.com", "force_new": True},
            201,
            {},
        ),
        (
            {"url": "http://www.example.com", "scrape_images": False},
            {"url": "http://www.example.com", "scrape_images": True},
            201,
            {"scrape_images": True},
        ),
        (
            {"url": "http://www.example.com", "scrape_images": True},
            {"url": "http://www.example.com", "scrape_images": False},
            303,
            {},
        ),
    ]
)
def test_create_duplicate_job(client, data1, data2, expected_status2, expected_data2):
    response = client.post('/scrape-jobs', json=data1)
    response = client.post('/scrape-jobs', json=data2)
    assert response.status_code == expected_status2
    if response.status_code == 200:
        assert all(item in response.json.items() for item in expected_data2.items())

def test_get_job_status(client):
    data = {"url": "http://www.example.com"}
    response = client.post('/scrape-jobs', json=data)
    assert response.status_code == 201
    job_id = response.json['id']
    response = client.get(f'/scrape-jobs/{job_id}')
    assert response.status_code == 200
    keys = ['id', 'url', 'is_finished', 'scrape_text', 'scrape_images']
    assert all(key in response.json for key in keys)

def test_get_text(client, prepopulated_db):
    response = client.get('/scrape-jobs/1/text')
    assert response.status_code == 200
    assert response.mimetype == 'text/plain'
    assert response.data == b'Hello world!'

    response = client.get('/scrape-jobs/2/text')
    assert response.status_code == 404

def test_get_images(client, prepopulated_db):
    response = client.get('/scrape-jobs/1/images')
    assert response.status_code == 200
    assert response.json == [1, 2]

    response = client.get('/scrape-jobs/2/images')
    assert response.status_code == 404

def test_get_image(client, prepopulated_db):
    response = client.get('/scrape-jobs/1/images/1')
    assert response.status_code == 200
    assert response.mimetype == 'image/jpeg'
    assert len(response.data) > 0

    response = client.get('/scrape-jobs/2/images/1')
    assert response.status_code == 404

