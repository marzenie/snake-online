import hashlib

def hash_str(str):
    sha256 = hashlib.sha256()
    sha256.update(str.encode('utf-8'))
    hashed_str = sha256.hexdigest()

    return hashed_str