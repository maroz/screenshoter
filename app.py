from flasgger import Swagger
from flask import Flask
from api.route.screenshot import screenshot_api
from api.route.stream_api import stream_api
from api.route.welcome import welcome


def create_app():
    app = Flask(__name__)
    Swagger(app,
            template={"info": {"title": "Screenshot API",
                               "description": "Captures RTP video stream screenshots",
                               "version": "1.0"}
                      }
            )
    app.register_blueprint(screenshot_api, url_prefix="/")
    app.register_blueprint(welcome, url_prefix="/")
    app.register_blueprint(stream_api, url_prefix="/")

    return app


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-p", "--port",
                        default=5000,
                        type=int,
                        help="port to listen on")
    args = parser.parse_args()
    port = args.port

    app = create_app()
    app.run(host="0.0.0.0", port=port)
