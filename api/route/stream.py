from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse

from utils.video_stream_helper import stream_helper


stream_router = APIRouter()


@stream_router.post("/start_stream/",
                    description="Endpoint to start a stream")
def start_stream(host: str = Form(default="127.0.0.1"), port: int = Form(default=5600)):
    stream_helper.host = host
    stream_helper.port = port
    stream_helper.start_stream()
    return RedirectResponse(url="/", status_code=303)



@stream_router.post("/stop_stream/",
                    description="Endpoint to stop a stream")
def stop_stream():
    stream_helper.stop_stream()
    return RedirectResponse(url="/", status_code=303)
