from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from db import db_connect, view

async def homepage(request):
    print('---------',request.method)
    data = view("""select * from users;""", 'one')
    
    return JSONResponse({'data': data})


app = Starlette(debug=True, routes=[
    Route('/hello', homepage, methods=["GET", "POST"]),
])
