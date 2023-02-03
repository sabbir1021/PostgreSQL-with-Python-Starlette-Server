from starlette.responses import JSONResponse
from database.db import view_all, view_details, create, update
from base.utils import has_password, token_generate
from database.exists import exists_check


async def login(request):
    if request.method == "POST":
        request_data = await request.json()
        username = request_data.get('username')
        password = request_data.get('password')
        # User check
        if exists_check({'username': username}, 'users'):
            password = has_password(password)
            if exists_check({'username': username,'password':password}, 'users'):
                token = token_generate(username)
               
                return JSONResponse({'message': "SuccessFully Login", "token": token}, status_code=201)
            else:
                return JSONResponse({'message': "Password Is not Valid"}, status_code=400)
        else:
            return JSONResponse({'message': "Username Is not Valid"}, status_code=400)
        
        
        data = {"message": f"Login faild {username}"}
        return JSONResponse({'data': data})

    data = {"message": "Login faild"}
    return JSONResponse({'data': data})