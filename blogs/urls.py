from starlette.routing import Route

from blogs.views import (
    homepage, 
    user_create_list, 
    user_retrieve_update, 
    blog_category_create_list, 
    blog_category_retrieve_update, 
    blog_tag_create_list, 
    blog_tag_retrieve_update, 
    blog_create_list, 
    blog_retrieve_update,
    blog_comment_create
)

blog_app = [
    Route('/hello', homepage, methods=["GET"]),

    Route('/users', user_create_list, methods=["GET", "POST"]),
    Route('/user/{user_id:int}', user_retrieve_update, methods=["GET", "PATCH"]),

    Route('/category', blog_category_create_list, methods=["GET", "POST"]),
    Route('/category/{category_id:int}', blog_category_retrieve_update, methods=["GET", "PATCH"]),

    Route('/tag', blog_tag_create_list, methods=["GET", "POST"]),
    Route('/tag/{tag_id:int}', blog_tag_retrieve_update, methods=["GET", "PATCH"]),

    Route('/blog', blog_create_list, methods=["GET", "POST"]),
    Route('/blog/{blog_id:int}', blog_retrieve_update, methods=["GET", "PATCH"]),

    Route('/blog-comment', blog_comment_create, methods=["POST"]),
]