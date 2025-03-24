import os
from flask import current_app
from werkzeug.utils import secure_filename
from app.models import db, File
from app.errors.exceptions import FileSaveError, DatabaseCommitError

def handle_file_upload(file, password):
    try:
        filename = secure_filename(file.filename)
        file_record = File(filename=filename)
        file_record.set_password(password)
        stored_filename = f"{file_record.uuid}_{filename}"
        file_record.stored_filename = stored_filename

        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], stored_filename)
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        try:
            file.save(upload_path)
        except Exception as e:
            raise FileSaveError(f"Failed to save file: {str(e)}")

        db.session.add(file_record)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DatabaseCommitError(f"Failed to commit to DB: {str(e)}")

        return file_record

    except Exception as e:
        raise e
