'''
This module contains the settings
'''

from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    '''Basic settings class'''
    testing: bool = False
    data_loader: Path = Path.home().joinpath(".annoto")


SETTINGS = Settings()
