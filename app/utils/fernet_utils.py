import os
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv
load_dotenv()
# Load key from environment or raise error
FERNET_SECRET_KEY = os.getenv("FERNET_SECRET_KEY")

if not FERNET_SECRET_KEY:
    raise ValueError("FERNET_SECRET_KEY not set in environment variables!")

fernet = Fernet(FERNET_SECRET_KEY)

def verify_fernet_token(token: str, ttl: int = 600) -> bool:
    """
    Decrypts and verifies a Fernet token.
    ttl = 60 means token expires after 60 seconds.
    """
    try:
        fernet.decrypt(token.encode(), ttl=ttl)
        return True
    except InvalidToken:
        return False
    except Exception:
        return False

def generate_token(payload: str) -> str:
    """(Optional) Utility to generate encrypted tokens for testing."""
    return fernet.encrypt(payload.encode()).decode()
