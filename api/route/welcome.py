from flask import render_template, Blueprint
from utils.video_stream_helper import stream_helper
welcome = Blueprint("welcome", __name__)


@welcome.route("/", methods=["GET"])
def index():
    stream_status = "🟢 Running" if stream_helper and stream_helper.is_running() else "🔴 Stopped"
    return render_template("index.html",
                           stream_status=stream_status,
                           stream_host=stream_helper.host,
                           stream_port=stream_helper.port)
