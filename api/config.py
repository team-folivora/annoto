from pathlib import Path
import tempfile


class Config(object):
    TESTING = False

class ProductionConfig(Config):
    DATA_FOLDER = str(Path.home().joinpath(".annoto"))

class DevelopmentConfig(Config):
    DATA_FOLDER = str(Path.home().joinpath(".annoto"))

class TestingConfig(Config):
    DATA_FOLDER = str(tempfile.mkdtemp(prefix="annoto"))
    TESTING = True
