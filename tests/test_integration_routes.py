import io
import os
from bs4 import BeautifulSoup
from app.models import File

def extract_csrf_token(response_data):
    """Extract CSRF token from form HTML."""
    soup = BeautifulSoup(response_data, 'html.parser')
    token_input = soup.find('input', {'name': 'csrf_token'})
    return token_input['value'] if token_input else None

def test_file_upload(client, app):
    get_response = client.get('/')
    csrf_token = extract_csrf_token(get_response.data.decode())

    data = {
        'file': (io.BytesIO(b"test content"), 'test.txt'),
        'password': 'testpass',
        'csrf_token': csrf_token
    }

    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        file_record = File.query.first()
        assert file_record is not None
        assert file_record.filename == 'test.txt'
        assert file_record.check_password('testpass')
        stored_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_record.stored_filename)
        assert os.path.exists(stored_file_path)

def test_file_download_wrong_password(client, app):
    get_response = client.get('/')
    csrf_token = extract_csrf_token(get_response.data.decode())

    data = {
        'file': (io.BytesIO(b"test content"), 'test.txt'),
        'password': 'testpass',
        'csrf_token': csrf_token
    }

    client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)

    with app.app_context():
        file_record = File.query.first()
        download_url = f'/get-file/{file_record.uuid}'

    get_form = client.get(download_url)
    csrf_token = extract_csrf_token(get_form.data.decode())

    response = client.post(download_url, data={
        'password': 'wrongpass',
        'csrf_token': csrf_token
    }, follow_redirects=True)

    assert response.status_code == 200

def test_file_download_correct_password(client, app):
    get_response = client.get('/')
    csrf_token = extract_csrf_token(get_response.data.decode())

    data = {
        'file': (io.BytesIO(b"test content"), 'test.txt'),
        'password': 'testpass',
        'csrf_token': csrf_token
    }

    client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)

    with app.app_context():
        file_record = File.query.first()
        download_url = f'/get-file/{file_record.uuid}'

    get_form = client.get(download_url)
    csrf_token = extract_csrf_token(get_form.data.decode())

    response = client.post(download_url, data={
        'password': 'testpass',
        'csrf_token': csrf_token
    }, follow_redirects=True)

    assert response.status_code == 200
    assert response.data == b"test content"
    assert f'attachment; filename={file_record.stored_filename}' in response.headers.get('Content-Disposition', '')

def test_upload_missing_file(client):
    get_response = client.get('/')
    csrf_token = extract_csrf_token(get_response.data.decode())

    response = client.post('/', data={
        'password': 'testpass',
        'csrf_token': csrf_token
    }, content_type='multipart/form-data', follow_redirects=True)

    assert b'This field is required.' in response.data or b'No file part' in response.data

def test_upload_missing_password(client):
    get_response = client.get('/')
    csrf_token = extract_csrf_token(get_response.data.decode())

    data = {
        'file': (io.BytesIO(b"test content"), 'test.txt'),
        'csrf_token': csrf_token
    }

    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b'This field is required.' in response.data or b'password is required' in response.data

def test_upload_disallowed_file_type(client):
    get_response = client.get('/')
    csrf_token = extract_csrf_token(get_response.data.decode())

    data = {
        'file': (io.BytesIO(b"test content"), 'malicious.exe'),
        'password': 'testpass',
        'csrf_token': csrf_token
    }

    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b'Allowed file types' in response.data

def test_upload_empty_filename(client):
    get_response = client.get('/')
    csrf_token = extract_csrf_token(get_response.data.decode())

    data = {
        'file': (io.BytesIO(b"test content"), ''),
        'password': 'testpass',
        'csrf_token': csrf_token
    }

    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b'No selected file' in response.data or b'This field is required.' in response.data

def test_upload_shows_success_page_with_link(client, app):
    get_response = client.get('/')
    csrf_token = extract_csrf_token(get_response.data.decode())

    data = {
        'file': (io.BytesIO(b"test content"), 'success.txt'),
        'password': 'strongpass',
        'csrf_token': csrf_token
    }

    response = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    assert b'File Uploaded Successfully!' in response.data
    assert b'Access File' in response.data

    with app.app_context():
        file_record = File.query.first()
        assert file_record is not None
        assert bytes(file_record.uuid, 'utf-8') in response.data

def test_upload_file_too_large(client, app):
    get_response = client.get('/')
    csrf_token = extract_csrf_token(get_response.data.decode())

    large_file = io.BytesIO(b"x" * (16 * 1024 * 1024 + 1))

    data = {
        'file': (large_file, 'big_file.txt'),
        'password': 'testpass',
        'csrf_token': csrf_token
    }

    response = client.post(
        '/',
        data=data,
        content_type='multipart/form-data',
        follow_redirects=False
    )

    assert response.status_code == 413
