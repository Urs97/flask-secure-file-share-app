import os
import shutil
import pytest
from app import create_app
from app.models import db
from app.config import TestConfig

@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.create_all()

        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        yield app

        db.session.remove()
        db.drop_all()

        if os.path.exists(upload_folder):
            try:
                shutil.rmtree(upload_folder)
            except Exception as e:
                print(f'Failed to remove upload folder {upload_folder}. Reason: {e}')

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
