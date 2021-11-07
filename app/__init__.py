from flask import Flask
from config import *
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='FDG#32fewg234v..21f',
    )

    cors = CORS(app, resources={
        r"/v1/meet/*": {"origins": "*"},
        r"/v1/recruit/*": {"origins": "*"},
        r"/v1/welink/subscription/*": {"origins": "*"}
    })

    app.config.from_object(flaskConfig)

    from app.error_handler import bp as err_bp
    app.register_blueprint(err_bp)

    from app.v1 import v1
    app.register_blueprint(v1)

    @app.route('/')
    def hello():
        return {
            "code": 0,
            "msg": "91-USST API"
        }

    return app
