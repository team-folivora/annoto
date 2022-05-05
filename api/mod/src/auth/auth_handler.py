import time
from typing import Dict, Optional

import jwt

from mod.src.settings import SETTINGS


class JWTPayload:
    user_id: str
    expires: float

    def __init__(self, user_id: str, expires: float):
        self.user_id = user_id
        self.expires = expires


def signJWT(user_id: str) -> str:
    payload = JWTPayload(user_id, time.time() + SETTINGS.jwt_expiry)
    token = jwt.encode(
        payload.__dict__, SETTINGS.jwt_secret, algorithm=SETTINGS.jwt_algorithm
    )
    return token


def decodeJWT(token: str) -> Optional[JWTPayload]:
    try:
        decoded_token = jwt.decode(
            token, SETTINGS.jwt_secret, algorithms=[SETTINGS.jwt_algorithm]
        )
        return (
            JWTPayload(**decoded_token)
            if decoded_token["expires"] >= time.time()
            else None
        )
    except:
        return None
