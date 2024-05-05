import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../flask-app')))
import pytest
from flask import Flask, jsonify
import auth
from auth import register, login, verify_password
from unittest.mock import patch, MagicMock, PropertyMock


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield

@patch('auth.users_collection.find_one')
def test_verify_password_correct(mock_find_one, app_context):
    # Mock the bcrypt hash checking
    with patch('bcrypt.hashpw') as mock_hashpw:
        mock_hashpw.return_value = b'$2b$12$CiuMJSqFmhoeB04pOiyHWe9hU8UkYS2YP/axz/1UGfQo8xiFv2Uma'
        mock_find_one.return_value = {"username": "user", "password": "$2b$12$CiuMJSqFmhoeB04pOiyHWe9hU8UkYS2YP/axz/1UGfQo8xiFv2Uma"}
        assert verify_password("user", "password") is not False

@patch('auth.users_collection.find_one')
def test_verify_password_incorrect(mock_find_one, app):
    mock_find_one.return_value = {"username": "user", "password": "$2b$12$CiuMJSqFmhoeB04pOiyHWe9hU8UkYS2YP/axz/1UGfQo8xiFv2Uma"}
    with app.app_context():
        assert not verify_password("user", "wrongpassword")

@patch('auth.users_collection.find_one')
def test_login_user_not_found(mock_find_one, app_context):
    mock_find_one.return_value = None
    response = login("nonexistent", "password")
    assert response[1] == 404  # HTTP 404 Not Found
