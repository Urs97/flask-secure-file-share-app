from flask import flash, redirect, request, url_for, current_app
from werkzeug.exceptions import RequestEntityTooLarge
from app.errors.exceptions import (
    InvalidPasswordError,
    FileMissingError,
    FileSaveError,
    DatabaseCommitError
)

def register_error_handlers(app):
    @app.errorhandler(InvalidPasswordError)
    def handle_invalid_password(error):
        flash("Incorrect password. Please try again.", "error")
        return redirect(request.referrer or url_for('main.index'))

    @app.errorhandler(FileMissingError)
    def handle_file_missing(error):
        flash("File not found on server.", "error")
        return redirect(request.referrer or url_for('main.index'))

    @app.errorhandler(FileSaveError)
    def handle_file_save_error(error):
        flash(str(error), "error")
        return redirect(request.referrer or url_for('main.index'))

    @app.errorhandler(DatabaseCommitError)
    def handle_db_commit_error(error):
        flash(str(error), "error")
        return redirect(request.referrer or url_for('main.index'))

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(error):
        flash("File is too large. Maximum allowed size is 16MB.", "error")
        return redirect(request.referrer or url_for('main.index')), 413

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        current_app.logger.exception("Unexpected error:")
        flash("An unexpected error occurred. Please try again later.", "error")
        return redirect(request.referrer or url_for('main.index'))
