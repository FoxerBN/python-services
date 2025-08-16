from app.util.decode_access_token import decode_access_token

def get_username_from_token(token: str) -> dict | None:
    """Decode token and return user_id & username"""
    return decode_access_token(token)
