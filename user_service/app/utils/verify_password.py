import hashlib

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Method to verify a password.
    
    Args:
        plain_password (str): The plain password.
        hashed_password (str): The hashed password.
    
    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
