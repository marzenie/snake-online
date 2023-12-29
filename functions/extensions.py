import hashlib
import random
import string

def hash_str(str):
    sha256 = hashlib.sha256()
    sha256.update(str.encode('utf-8'))
    hashed_str = sha256.hexdigest()

    return hashed_str


def generate_random(length, use_special_chars=True):
    characters = string.ascii_letters + string.digits
    if use_special_chars:
        characters += string.punctuation

    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

def split_jsons(json_string):
    json_objects = []
    depth = 0
    start = 0

    for i, char in enumerate(json_string):
        if char == '{':
            if depth == 0:
                start = i
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                json_objects.append(json_string[start:i+1])

    return json_objects