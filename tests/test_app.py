# import pytest
import sys
import os
sys.path.append(os.path.abspath('../'))
# from app import main


import pytest
import app
from flask import Flask

@pytest.fixture
def client():
    sut = app.get_app()

    with sut.test_client() as client:
        yield client

def test_ping(client):
    response = client.get('/ping')
    expected = os.getenv('PING_RESPONSE', 'pong\n')
    assert response.data.decode('utf-8') == expected
    assert response.status_code == 200