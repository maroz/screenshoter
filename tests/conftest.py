import pytest

from app import create_app
from utils.video_stream_helper import stream_helper


@pytest.fixture
def app():
    return create_app()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def video_stream_host():
    return "127.0.0.1"


@pytest.fixture()
def video_stream_port():
    return 5600


@pytest.fixture()
def video_stream_helper(video_stream_host, video_stream_port):
    stream_helper.host = video_stream_host
    stream_helper.port = video_stream_port
    return stream_helper


@pytest.fixture()
def start_stream(video_stream_helper):
    video_stream_helper.start_stream()
    yield
    video_stream_helper.stop_stream()
