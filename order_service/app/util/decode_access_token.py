import os
import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')

def decode_access_token(token: str) -> dict | None:
    """Decode token and return username"""
    if not token or not SECRET_KEY:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "user_id": payload.get('user_id'),
            "username": payload.get('sub')
        }
    except jwt.ExpiredSignatureError:
        print("❌ Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"❌ Invalid token: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None
