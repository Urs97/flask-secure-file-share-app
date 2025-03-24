import io
import os
from werkzeug.datastructures import FileStorage
from app.services.file_upload_service import handle_file_upload
from app.models import File

def test_handle_file_upload_creates_record(app):
    file = FileStorage(stream=io.BytesIO(b"test content"), filename="example.txt")
    password = "securepass"

    with app.app_context():
        file_record = handle_file_upload(file, password)

        assert isinstance(file_record, File)
        assert file_record.filename == "example.txt"
        assert file_record.check_password(password)

        saved_path = os.path.join(app.config["UPLOAD_FOLDER"], file_record.stored_filename)
        assert os.path.exists(saved_path)
