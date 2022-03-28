from pathlib import Path
from typing import Optional
from flask import Flask, send_file


def create_app(config_object: str = None):
    app = Flask(__name__)
    if app.config["ENV"] == "development":
        app.config.from_object("api.config.DevelopmentConfig")
    elif app.config["ENV"] == "production":
        app.config.from_object("api.config.ProductionConfig")
    else:
        app.config.from_object(config_object)

    @app.route('/image')
    def index():
        '''Responds with a random image from the users ~/.annoto folder'''
        image_path = Path(app.config["DATA_FOLDER"]).joinpath("sloth.jpg")
        return send_file(str(image_path), mimetype='image/jpg')

    return app
