from pathlib import Path
from flask import Flask, send_file


def create_app():
    app = Flask(__name__)


    @app.route('/image')
    def index():
        '''Responds with a random image from the users ~/.annoto folder'''
        home = Path.home()
        home = home.joinpath(".annoto").joinpath("sloth.jpg")
        return send_file(str(home), mimetype='image/jpg')

    return app
