
import hashlib

from django.utils import timezone

from eazyinvoice.secrets import get_cors_secret_int


def create_md5_hash(s: str) -> str:
    result = hashlib.md5(s.encode())
    return result.hexdigest()


class InvalidSecretToken(Exception):
    pass

def validate_secret_token(val: str) -> None:
    try:
        int_val = int(val)
    except ValueError:
        raise InvalidSecretToken
    
    if int_val % get_cors_secret_int() != 0:
        raise InvalidSecretToken
