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
    assert response.data == b"pong\n"
    assert response.status_code == 200