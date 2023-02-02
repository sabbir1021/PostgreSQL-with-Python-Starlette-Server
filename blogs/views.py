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
            return JSONResponse(data, status_code=400)
        else:
            return JSONResponse(data, status_code=200)

    if request.method == "POST":
        request_data = await request.json()
        username = request_data.get('username')
        phone = request_data.get('phone')
        email = request_data.get('email')
        values = (username, phone, email)
        query = """INSERT INTO users(username, phone, email) VALUES (%s,%s,%s) RETURNING id, username, phone, email"""
        data = create(query, values)
        return JSONResponse(data, status_code=201)
    
    # return JSONResponse(data)


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
    
    return JSONResponse(data, status_code=201)


# Category

async def blog_category_create_list(request):
    if request.method == "GET":
        page_size = request.query_params.get('page_size')
        page = request.query_params.get('page')
        search = request.query_params.get('search')
        search_fields = ['name']
        # created_by = request.query_params.get('created_by')
        # filter_fields = {'created_by': created_by}
        
        query = """select blog_categories.id, blog_categories.name, blog_categories.show_in, users.id as created_by_id,
            users.username as created_by_username, users.email as created_by_email, users.phone as created_by_phone
            from blog_categories
            inner join users on blog_categories.created_by = users.id"""
        table = "blog_categories"
        data = view_all(query, table, page_size, page, search, search_fields)
        
        if data.get('status') != 200:
            data.pop('status')
            return JSONResponse(data, status_code=400)
        else:
            data.pop('status')
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
        values = (name, created_by, show_in)
        query = """INSERT INTO blog_categories(name, created_by, show_in) VALUES (%s,%s,%s) RETURNING id, name, created_by, show_in"""
        data = create(query, values)
    return JSONResponse(data, status_code=200)


async def blog_category_retrieve_update(request):
    if request.method == "GET":
        category_id = request.path_params['category_id']
        data = view_details("""select * from blog_categories WHERE blog_categories.id = {};""".format(category_id))

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
    
    return JSONResponse(data, status_code=200)


# Blog Tags

async def blog_tag_create_list(request):
    if request.method == "GET":
        page_size = request.query_params.get('page_size')
        page = request.query_params.get('page')
        search = request.query_params.get('search')
        search_fields = ['name']
        # created_by = request.query_params.get('created_by')
        # filter_fields = {'created_by': created_by}
        
        query = """select blog_tags.id, blog_tags.name, blog_tags.show_in, users.id as created_by_id,
            users.username as created_by_username, users.email as created_by_email, users.phone as created_by_phone
            from blog_tags
            inner join users on blog_tags.created_by = users.id"""
        table = "blog_tags"
        data = view_all(query, table, page_size, page, search, search_fields)
        
        if data.get('status') != 200:
            data.pop('status')
            return JSONResponse(data, status_code=400)
        else:
            data.pop('status')
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
        values = (name, created_by, show_in)
        query = """INSERT INTO blog_tags(name, created_by, show_in) VALUES (%s,%s,%s) RETURNING id, name, created_by, show_in"""
        data = create(query, values)
    return JSONResponse(data, status_code=200)


async def blog_tag_retrieve_update(request):
    if request.method == "GET":
        tag_id = request.path_params['tag_id']
        query = """select blog_tags.id, blog_tags.name, blog_tags.show_in, users.id as created_by_id,
            users.username as created_by_username, users.email as created_by_email, users.phone as created_by_phone
            from blog_tags
            inner join users on blog_tags.created_by = users.id 
            WHERE blog_tags.id = {}""".format(tag_id)
        data = view_details(query)
        user = {}
        user['id'] = data.get('data').pop("created_by_id")
        user['username'] = data.get('data').pop("created_by_username")
        user['email'] = data.get('data').pop("created_by_email")
        user['phone'] = data.get('data').pop("created_by_phone")
        data.get('data')['created_by'] = user

    if request.method == "PATCH":
        tag_id = request.path_params['tag_id']
        request_data = await request.json()

        change_data = ""
        for key, value in request_data.items():
            if isinstance(value, str):
                change_data = change_data + key + " = " + f"'{value}'" + ", "
            else:
                change_data = change_data + key + " = " + f"{value}" + ", "


        sql_text = f"UPDATE blog_tags SET {change_data[0:-2]} WHERE blog_tags.id = {tag_id};"
        data = update("""{}""".format(sql_text))
    
    return JSONResponse(data, status_code=200)


# Blog


async def blog_create_list(request):
    if request.method == "GET":
        page_size = request.query_params.get('page_size')
        page = request.query_params.get('page')
        search = request.query_params.get('search')
        search_fields = ['title']
        # created_by = request.query_params.get('created_by')
        # filter_fields = {'created_by': created_by}
        
        query = """select blogs.id, blogs.title, blogs.description, blogs.thumbnail, TO_CHAR(blogs.publish_date, 'YYYY-MM-DD HH24:MI:SS') as publish_date, blogs.show_in, blog_categories.id as category_id, blog_categories.name as category_name, users.id as created_by_id,
            users.username as created_by_username, users.email as created_by_email, users.phone as created_by_phone, 
            
            (SELECT json_agg(json_build_object('id', blog_tags.id,'name', blog_tags.name))
            FROM blogs_tags
            INNER JOIN blog_tags ON blogs_tags.tag = blog_tags.id
            where blogs_tags.blog = blogs.id
            ) AS tags

            from blogs
            inner join users on blogs.created_by = users.id
            inner join blog_categories on blogs.category = blog_categories.id
            """
        table = "blogs"
        data = view_all(query, table, page_size, page, search, search_fields)
        
        if data.get('status') != 200:
            data.pop('status')
            return JSONResponse(data, status_code=400)
        else:
            data.pop('status')
        for i in data.get('data'):
            category = {}
            category['id'] = i.pop("category_id")
            category['name'] = i.pop("category_name")
            i['category'] = category
            user = {}
            user['id'] = i.pop("created_by_id")
            user['username'] = i.pop("created_by_username")
            user['email'] = i.pop("created_by_email")
            user['phone'] = i.pop("created_by_phone")
            i['created_by'] = user


    if request.method == "POST":
        request_data = await request.json()
        title = request_data.get('title')
        description = request_data.get('description')
        thumbnail = request_data.get('thumbnail')
        category = request_data.get('category')
        created_by = request_data.get('created_by')
        show_in = request_data.get('show_in')
        publish_date = request_data.get('publish_date')
        tags = request_data.get('tags')
        values = (title, description, thumbnail, category, created_by, show_in, publish_date)
        query = """INSERT INTO blogs(title, description, thumbnail, category, created_by, show_in, publish_date) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id, title, description, thumbnail"""
        data = create(query, values)
        
        for i in tags:
            blog_id = data.get('data').get('id')
            print(blog_id)
            values = (blog_id, i)
            query = """INSERT INTO blogs_tags(blog, tag) VALUES (%s,%s) RETURNING id, blog, tag"""
            tag_data = create(query, values)
            print(tag_data)

       

    return JSONResponse(data, status_code=200)


async def blog_retrieve_update(request):
    if request.method == "GET":
        blog_id = request.path_params['blog_id']
        query = """select  blogs.id, blogs.title, blogs.description, blogs.thumbnail, TO_CHAR(blogs.publish_date, 'YYYY-MM-DD HH24:MI:SS') as publish_date, blogs.show_in, blog_categories.id as category_id, blog_categories.name as category_name, users.id as created_by_id,
            users.username as created_by_username, users.email as created_by_email, users.phone as created_by_phone
            from blogs
            inner join users on blogs.created_by = users.id
            inner join blog_categories on blogs.category = blog_categories.id
            WHERE blogs.id = {}""".format(blog_id)
        data = view_details(query)
        category = {}
        category['id'] = data.get('data').pop("category_id")
        category['name'] = data.get('data').pop("category_name")
        data.get('data')['category'] = category
        user = {}
        user['id'] = data.get('data').pop("created_by_id")
        user['username'] = data.get('data').pop("created_by_username")
        user['email'] = data.get('data').pop("created_by_email")
        user['phone'] = data.get('data').pop("created_by_phone")
        data.get('data')['created_by'] = user


    if request.method == "PATCH":
        blog_id = request.path_params['blog_id']
        request_data = await request.json()

        change_data = ""
        for key, value in request_data.items():
            if isinstance(value, str):
                change_data = change_data + key + " = " + f"'{value}'" + ", "
            else:
                change_data = change_data + key + " = " + f"{value}" + ", "


        sql_text = f"UPDATE blogs SET {change_data[0:-2]} WHERE blogs.id = {blog_id};"
        data = update("""{}""".format(sql_text))
    
    return JSONResponse(data, status_code=200)