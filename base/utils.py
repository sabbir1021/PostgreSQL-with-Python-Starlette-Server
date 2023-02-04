import hashlib
import datetime
from datetime import timedelta
from database.db import create, view_details
import uuid
import base64
import json

def has_password(value):
    plaintext = value.encode()
    d = hashlib.sha256(plaintext)
    data = d.hexdigest()
    print(data)
    return data

def token_generate(username):
    token_id = str(uuid.uuid1())
    valid_time = datetime.datetime.now() + timedelta(minutes=1)
    print(valid_time)

    user = view_details("""select id, username, phone, email, first_name, last_name from users WHERE users.username = '{}';""".format(username)).get('data')
    
    # user object to decode.
    user['token_id'] = token_id
    user['valid_time'] = str(valid_time)
    user_bytes = json.dumps(user).encode('utf-8')
    user_base64_bytes = base64.b64encode(user_bytes)
    token_base64_string = user_base64_bytes.decode("ascii")

    values = (user.get('id'), token_id, token_base64_string, valid_time)
    query = """INSERT INTO user_token(user_id, token_id, token, valid_time) VALUES (%s,%s,%s,%s) RETURNING * """
    data = create(query, values)
    if data.get('status') == 400:
        return data
    else:
        data = data.get('data').get('token')
    return data


def token_validation_check(token):
    token_bytes = token.encode("ascii")
    token_bytes_data = base64.b64decode(token_bytes)
    token_data = token_bytes_data.decode("ascii")
    token_dict_data = json.loads(token_data)    
    if datetime.datetime.now() <= datetime.datetime.strptime(token_dict_data.get('valid_time'), '%Y-%m-%d %H:%M:%S.%f'):
        return True
    else:
        return False

def is_authenticated(token):
    token = token
    valid = token_validation_check(token)
    if valid:
        return True
    else:
        return False
