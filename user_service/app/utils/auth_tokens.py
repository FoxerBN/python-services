import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "12345")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def create_access_token(username: str, user_id: int, expires: timedelta = timedelta(hours=3)) -> str:
    """Create an access token for the given user."""
    payload = {
        "sub": username,
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + expires,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> str | None:
    """Decode an access token and return the username if valid."""    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
