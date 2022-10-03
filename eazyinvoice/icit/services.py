
import hashlib

def create_md5_hash(s: str) -> str:
    result = hashlib.md5(s.encode())
    return result.hexdigest()
