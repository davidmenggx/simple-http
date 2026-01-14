import hashlib

def get_etag(content: bytes) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(content)
    return sha256_hash.hexdigest()