from starlette.responses import JSONResponse
from database.db import view_all, view_details, create, update
from base.utils import has_password
from database.exists import exists_check
import random
import datetime
from datetime import timedelta

async def login(request):
    if request.method == "POST":
        request_data = await request.json()
        username = request_data.get('username')
        password = request_data.get('password')
        # User check
        if exists_check({'username': username}, 'users'):
            password = has_password(password)
            if exists_check({'username': username,'password':password}, 'users'):
                token = random.randrange(100000, 500000)
                user_id = view_details("""select * from users WHERE users.username = '{}';""".format(username)).get('data').get('id')
                valid_time = datetime.datetime.now() + timedelta(hours=1)
                values = (user_id, token, valid_time)
                query = """INSERT INTO user_token(user_id, token, valid_time) VALUES (%s,%s,%s) RETURNING * """
                data = create(query, values)
                print(data)
               
                return JSONResponse({'message': "SuccessFully Login", "token": data.get('data').get('token')}, status_code=201)
            else:
                return JSONResponse({'message': "Password Is not Valid"}, status_code=400)
        else:
            return JSONResponse({'message': "Username Is not Valid"}, status_code=400)
        
        
        data = {"message": f"Login faild {username}"}
        return JSONResponse({'data': data})

    data = {"message": "Login faild"}
    return JSONResponse({'data': data})