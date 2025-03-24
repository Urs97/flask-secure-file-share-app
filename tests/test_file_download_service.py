import io
import os
from werkzeug.datastructures import FileStorage
from app.services.file_upload_service import handle_file_upload
from app.services.file_download_service import handle_file_download
from app.errors.exceptions import InvalidPasswordError, FileMissingError

def test_handle_file_download_success(app):
    file = FileStorage(stream=io.BytesIO(b"content"), filename="test.txt")
    with app.app_context():
        file_record = handle_file_upload(file, "pass")
        with app.test_request_context():
            response = handle_file_download(file_record, "pass")
            assert response.status_code == 200
            assert response.headers["Content-Disposition"].startswith("attachment")

def test_handle_file_download_invalid_password(app):
    file = FileStorage(stream=io.BytesIO(b"secret"), filename="wrongpass.txt")
    with app.app_context():
        file_record = handle_file_upload(file, "rightpass")

        try:
            handle_file_download(file_record, "wrongpass")
            assert False, "Expected InvalidPasswordError"
        except InvalidPasswordError:
            pass

def test_handle_file_download_missing_file(app):
    file = FileStorage(stream=io.BytesIO(b"missing"), filename="ghost.txt")
    with app.app_context():
        file_record = handle_file_upload(file, "ghostpass")

        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], file_record.stored_filename))

        try:
            handle_file_download(file_record, "ghostpass")
            assert False, "Expected FileMissingError"
        except FileMissingError:
            pass
