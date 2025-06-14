from flasgger import swag_from
from flask import Blueprint, send_file, request
from io import BytesIO

from utils.video_stream_helper import stream_helper

screenshot_api = Blueprint("screenshot_api", __name__)

@screenshot_api.route("/screenshot/", methods=["GET"])
@swag_from({
    "tags": ["Screenshot"],
    "parameters": [
        {
            "name": "host",
            "in": "query",
            "type": "string",
            "required": False,
            "default": "127.0.0.1",
            "description": "Video stream host"
        },
        {
            "name": "port",
            "in": "query",
            "type": "integer",
            "required": False,
            "default": 5600,
            "description": "Video stream port"
        }
    ],
    "responses": {
        200: {
            "description": "A PNG screenshot from the stream",
            "content": {
                "image/png": {
                    "schema": {
                        "type": "string",
                        "format": "binary"
                    }
                }
            }
        },
        400: {"description": "Invalid input"},
        500: {"description": "Screenshot capture failed"}
    }
})
def get_screenshot():
    query_params = request.args.to_dict()
    host = query_params.get("host", "127.0.0.1")
    try:
        port = int(query_params.get("port", 5600))
    except ValueError:
        return {"error": "Invalid port value"}, 400

    try:
        timestamp, image_bytes = stream_helper.capture_screenshot(host=host, port=port)
    except Exception as e:
        return {"error": f"Screenshot capture failed: {str(e)}"}, 500

    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp_str}.png"

    return send_file(BytesIO(image_bytes),
                     download_name=filename,
                     as_attachment=True,
                     mimetype="image/png")
