'''
Basic configuration classes for the flask app
'''

from pathlib import Path
import tempfile

#pylint-ignore: too-few-public-methods

class Config:
    '''Base Config class'''
    TESTING = False
    DATA_FOLDER = str(Path.home().joinpath(".annoto"))

class ProductionConfig(Config):
    '''Production Config class'''

class DevelopmentConfig(Config):
    '''Development Config class'''

class TestingConfig(Config):
    '''Testing Config class'''
    DATA_FOLDER = str(tempfile.mkdtemp(prefix="annoto"))
    TESTING = True
