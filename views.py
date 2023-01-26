from starlette.responses import JSONResponse
from starlette.responses import Response
from db import db_connect, view, create, update
import json


async def homepage(request):
    data = {
        "message": "Home page"
    }
    return JSONResponse({'data': data})


async def user_create_list(request):
    if request.method == "GET":
        data = view("""select * from users;""")

    if request.method == "POST":
        request_data = await request.json()
        username = request_data.get('username')
        phone = request_data.get('phone')
        email = request_data.get('email')
        data = create(""" INSERT INTO users(username, phone, email) VALUES ('{}','{}', '{}')""".format(username,phone,email))
    
    return JSONResponse({'data': data})


async def user_retrieve_update(request):
    if request.method == "GET":
        user_id = request.path_params['user_id']
        data = view("""select * from users WHERE users.id = {};""".format(user_id), 'one')

    if request.method == "PATCH":
        user_id = request.path_params['user_id']
        request_data = await request.json()

        change_data = ""
        for key, value in request_data.items():
            if isinstance(value, str):
                change_data = change_data + key + " = " + f"'{value}'" + ", "
            else:
                change_data = change_data + key + " = " + f"{value}" + ", "


        sql_text = f"UPDATE users SET {change_data[0:-2]} WHERE users.id = {user_id};"
        data = create("""{}""".format(sql_text))
    
    return JSONResponse({'data': data})


# Category

async def blog_category_create_list(request):
    if request.method == "GET":
        data = view("""select * from blog_categories;""")

    if request.method == "POST":
        request_data = await request.json()
        name = request_data.get('name')
        created_by = request_data.get('created_by')
        show_in = request_data.get('show_in')
        data = create(""" INSERT INTO blog_categories(name, created_by, show_in) VALUES ('{}','{}', '{}')""".format(name,created_by, show_in))
    
    return JSONResponse({'data': data})


async def blog_category_retrieve_update(request):
    if request.method == "GET":
        category_id = request.path_params['category_id']
        data = view("""select * from blog_categories WHERE blog_categories.id = {};""".format(category_id), 'one')

    if request.method == "PATCH":
        category_id = request.path_params['category_id']
        request_data = await request.json()

        change_data = ""
        for key, value in request_data.items():
            if isinstance(value, str):
                change_data = change_data + key + " = " + f"'{value}'" + ", "
            else:
                change_data = change_data + key + " = " + f"{value}" + ", "


        sql_text = f"UPDATE blog_categories SET {change_data[0:-2]} WHERE blog_categories.id = {category_id};"
        data = create("""{}""".format(sql_text))
    
    return JSONResponse({'data': data})