import allure
import contextlib
import os
import subprocess
import tempfile
import threading

from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


sdp_content = """v=0
s=RTP Stream
c=IN IP4 {host}
t=0 0
m=video {port} RTP/AVP 96
a=rtpmap:96 H264/90000
"""


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class VideoStreamHelper(metaclass=Singleton):
    host: str = field(default="127.0.0.1")
    port: int = field(default=5600)
    thread: Optional[threading.Thread] = field(init=False, default=None)
    process: Optional[subprocess.Popen] = field(init=False, default=None)

    def __post_init__(self):
        assert self.host and self.port, "Host and port must be specified for the video stream"
        assert isinstance(self.port, int), "Port must be an integer"

    @property
    def cmd(self) -> list:
        return [
            "gst-launch-1.0", "videotestsrc",
            "!", "video/x-raw,width=1280,height=720",
            "!", "openh264enc",
            "!", "rtph264pay", "config-interval=1",
            "!", f"udpsink", f"host={self.host}", f"port={self.port}"
        ]

    @allure.step("Start video stream")
    def start_stream(self) -> None:
        if self.process is None:
            def run():
                self.process = subprocess.Popen(self.cmd)
                self.process.wait()
            self.thread = threading.Thread(target=run, daemon=True)
            self.thread.start()

    @allure.step("Stop video stream")
    def stop_stream(self) -> None:
        if self.process and self.process.poll() is None:
            self.process.kill()
            self.process.wait()
            self.process = None
            self.thread = None

    def is_running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    @staticmethod
    @allure.step("Capture screenshot from video stream")
    def capture_screenshot(host: str,
                           port: str) -> (datetime, bytes):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".sdp") as sdp_file:
            sdp_file.write(sdp_content.format(host=host,
                                              port=port))
            sdp_file_path = sdp_file.name

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as image_file:
            image_file_path = image_file.name

        try:
            current_time = datetime.now()
            subprocess.run([
                "ffmpeg", "-y",
                "-protocol_whitelist", "file,udp,rtp",
                "-i", sdp_file_path,
                "-vframes", "1",
                image_file_path
            ], check=True)

            with open(image_file_path, "rb") as f:
                return current_time, f.read()
        finally:
            os.remove(sdp_file_path)
            with contextlib.suppress(FileNotFoundError):
                os.remove(image_file_path)


stream_helper = VideoStreamHelper()
