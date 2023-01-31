from starlette.routing import Route
from starlette.applications import Starlette
from blogs.views import homepage, user_create_list, user_retrieve_update, blog_category_create_list, blog_category_retrieve_update

blog_app = [
    Route('/hello', homepage, methods=["GET"]),
    Route('/users', user_create_list, methods=["GET", "POST"]),
    Route('/user/{user_id:int}', user_retrieve_update, methods=["GET", "PATCH"]),

    Route('/category', blog_category_create_list, methods=["GET", "POST"]),
    Route('/category/{category_id:int}', blog_category_retrieve_update, methods=["GET", "PATCH"]),
]