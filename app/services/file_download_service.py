import os
from flask import current_app, send_from_directory
from app.errors.exceptions import InvalidPasswordError, FileMissingError

def handle_file_download(file_record, password):
    if not file_record.check_password(password):
        raise InvalidPasswordError("Incorrect password.")

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_record.stored_filename)

    if not os.path.exists(file_path):
        raise FileMissingError("File not found on server.")

    upload_folder = os.path.abspath(current_app.config['UPLOAD_FOLDER'])

    return send_from_directory(
        upload_folder,
        file_record.stored_filename,
        as_attachment=True
    )
