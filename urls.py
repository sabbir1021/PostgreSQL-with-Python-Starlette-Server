from starlette.routing import Route
from starlette.applications import Starlette
from blogs.urls import blog_app
from auth.urls import auth_app

app = Starlette(debug=True, routes=blog_app+auth_app)