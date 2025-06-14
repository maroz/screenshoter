from flasgger import swag_from
from flask import Blueprint, request, redirect, url_for

from utils.video_stream_helper import stream_helper

stream_api = Blueprint("stream_api", __name__)


@stream_api.route("/start_stream/", methods=["POST"])
@swag_from({
    "tags": ["Stream"],
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
            "description": "Stream started successfully",
            "content": {
                "text/html": {
                    "schema": {
                        "type": "string"
                    }
                }
            }
        },
        400: {"description": "Invalid input"},
        500: {"description": "Failed to start stream"}
    }
})
def start_stream():
    values = request.values.to_dict()
    host = values.get("host", "127.0.0.1")

    try:
        port = int(values.get("port", 5600))
    except ValueError:
        return {"error": "Invalid port value"}, 400

    stream_helper.host = host
    stream_helper.port = port
    stream_helper.start_stream()
    return redirect(url_for("welcome.index"))

@stream_api.route("/stop_stream/", methods=["POST"])
@swag_from({
    "tags": ["Stream"],
    "responses": {
        200: {
            "description": "Stream stopped successfully",
            "content": {
                "text/html": {
                    "schema": {
                        "type": "string"
                    }
                }
            }
        },
        500: {"description": "Failed to stop stream"}
    }
})
def stop_stream():
    stream_helper.stop_stream()
    return redirect(url_for("welcome.index"))
