from starlette.responses import JSONResponse
from starlette.responses import Response
from database.db import view_all, view_details, create, update
import json


async def homepage(request):
    data = {
        "message": "Home page"
    }
    return JSONResponse({'data': data})


async def user_create_list(request):
    if request.method == "GET":
        page_size = request.query_params.get('page_size')
        page = request.query_params.get('page')
        search = request.query_params.get('search')
        search_fields = ['username', 'email']
        query = """select * from users"""
        table = "users"
        data = view_all(query, table, page_size, page, search, search_fields)
        if data.get('status') != 200:
            return JSONResponse(data)

    if request.method == "POST":
        request_data = await request.json()
        username = request_data.get('username')
        phone = request_data.get('phone')
        email = request_data.get('email')
        values = (username, phone, email)
        query = """INSERT INTO users(username, phone, email) VALUES (%s,%s,%s) RETURNING id, username, phone, email"""
        data = create(query, values)
    
    return JSONResponse(data)


async def user_retrieve_update(request):
    if request.method == "GET":
        user_id = request.path_params['user_id']
        data = view_details("""select * from users WHERE users.id = {};""".format(user_id))

    if request.method == "PATCH":
        user_id = request.path_params['user_id']
        request_data = await request.json()

        change_data = ""
        for key, value in request_data.items():
            if isinstance(value, str):
                change_data = change_data + key + " = " + f"'{value}'" + ", "
            else:
                change_data = change_data + key + " = " + f"{value}" + ", "

        print(change_data)
        sql_text = f"UPDATE users SET {change_data[0:-2]} WHERE users.id = {user_id};"
        data = update("""{}""".format(sql_text))
    
    return JSONResponse(data)


# Category

async def blog_category_create_list(request):
    if request.method == "GET":
        page_size = request.query_params.get('page_size')
        page = request.query_params.get('page')
        search = request.query_params.get('search')
        search_fields = ['name']
        query = """select blog_categories.id, blog_categories.name, blog_categories.show_in, users.id as created_by_id,
            users.username as created_by_username, users.email as created_by_email, users.phone as created_by_phone
            from blog_categories
            inner join users on blog_categories.created_by = users.id"""
        table = "blog_categories"
        data = view_all(query, table, page_size, page, search, search_fields)
        if data.get('status') != 200:
            return JSONResponse(data)

        for i in data.get('data'):
            user = {}
            user['id'] = i.pop("created_by_id")
            user['username'] = i.pop("created_by_username")
            user['email'] = i.pop("created_by_email")
            user['phone'] = i.pop("created_by_phone")
            i['created_by'] = user

    if request.method == "POST":
        request_data = await request.json()
        name = request_data.get('name')
        created_by = request_data.get('created_by')
        show_in = request_data.get('show_in')
        data = create(""" INSERT INTO blog_categories(name, created_by, show_in) VALUES ('{}','{}', '{}')""".format(name,created_by, show_in))
    
    return JSONResponse(data)


async def blog_category_retrieve_update(request):
    if request.method == "GET":
        category_id = request.path_params['category_id']
        data = view_details("""select * from blog_categories WHERE blog_categories.id = {};""".format(category_id), 'one')

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
        data = update("""{}""".format(sql_text))
    
    return JSONResponse(data)