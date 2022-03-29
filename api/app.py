from pathlib import Path
from flask import Flask, send_file


def create_app(config_object: str = None):
    app = Flask(__name__)
    if config_object:
        app.config.from_object(config_object)
    elif app.config["ENV"] == "development":
        app.config.from_object("api.config.DevelopmentConfig")
    else:
        app.config.from_object("api.config.ProductionConfig")

    @app.route('/image')
    def index():
        '''Responds with a random image from the users ~/.annoto folder'''
        image_path = Path(app.config["DATA_FOLDER"]).joinpath("sloth.jpg")
        return send_file(str(image_path), mimetype='image/jpg')

    return app
