from fastapi import FastAPI
from api.route.home import home_router
from api.route.stream import (stream_router)
from api.route.screenshot import screenshot_router

app = FastAPI(title="Video Stream API",
              description="API for managing video streams and capturing screenshots",
              version="1.0.0")
app.include_router(home_router)
app.include_router(stream_router)
app.include_router(screenshot_router)
