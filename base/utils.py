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
    valid_time = datetime.datetime.now() + timedelta(hours=1)

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