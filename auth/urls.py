from starlette.routing import Route
from auth.views import (
   login
)


auth_app = [
    Route('/login', login, methods=["POST"]),
  
]