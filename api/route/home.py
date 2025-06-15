from fastapi import APIRouter, Request
from utils.video_stream_helper import stream_helper
from fastapi.templating import Jinja2Templates

home_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@home_router.get("/")
def index(request: Request):
    status = "🟢 Running" if stream_helper and stream_helper.is_running() else "🔴 Stopped"
    return templates.TemplateResponse(request=request,
                                      name="index.html",
                                      context={"stream_status": status,
                                               "stream_host": stream_helper.host,
                                               "stream_port": stream_helper.port})


@home_router.get("/stream_status/")
def stream_status():
    status = "🟢 Running" if stream_helper and stream_helper.is_running() else "🔴 Stopped"
    return {"status": status}
