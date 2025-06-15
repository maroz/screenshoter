from fastapi import Response, APIRouter, HTTPException

from utils.video_stream_helper import stream_helper


screenshot_router = APIRouter()


@screenshot_router.get("/screenshot")
def get_screenshot(host: str = "127.0.0.1", port: int = 5600):
    try:
        timestamp, image_bytes = stream_helper.capture_screenshot(host=host, port=port)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Screenshot capture failed: {str(e)}")

    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp_str}.png"

    return Response(
        image_bytes,
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
