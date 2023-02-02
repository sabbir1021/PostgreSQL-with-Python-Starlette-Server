import hashlib


def has_password(value):
    plaintext = value.encode()
    d = hashlib.sha256(plaintext)
    data = d.hexdigest()
    print(data)
    return data