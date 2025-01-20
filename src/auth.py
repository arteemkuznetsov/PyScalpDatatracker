import os

from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from jose import JWTError, jwt

load_dotenv()
security = HTTPBearer()


class Auth:
    secret_key: str
    algorithm: str

    def __init__(self) -> None:
        self.secret_key = os.getenv('AUTH_SECRET_KEY')
        self.algorithm = 'HS256'

    def create_access_token(self, database: str):
        to_encode = {'database': database}
        encoded_jwt = jwt.encode(to_encode, key=self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def check_access_token(self, credentials: HTTPBasicCredentials = Depends(HTTPBearer())):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        token = credentials.credentials

        try:
            payload = jwt.decode(
                token=token,
                key='secret',
                options={
                    'verify_signature': False,
                    'verify_aud': False,
                    'verify_iss': False
                }
            )
            if payload is None:
                raise credentials_exception
            return payload
        except JWTError:
            raise credentials_exception
