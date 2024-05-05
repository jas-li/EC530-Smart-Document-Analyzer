import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../flask-app')))
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
import secure_upload

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg'}
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@patch('secure_upload.MongoClient')
def test_allowed_file(mock_mongo_client, app):
    with app.app_context():
        assert secure_upload.allowed_file("test.txt")
        assert not secure_upload.allowed_file("test.exe")

@patch('secure_upload.MongoClient')
@patch('secure_upload.fs.put')
def test_process_file(mock_put, mock_mongo_client, app):
    mock_put.return_value = 'file_id_123'
    with app.app_context():
        file = MagicMock(filename="test.txt", content_type="text/plain")
        result = secure_upload.process_file(file)
        assert result == 'file_id_123'

