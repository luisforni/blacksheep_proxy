from blacksheep import Application, get
from app.api.middlewares.error_handler import error_middleware
from app.api.middlewares.auth_jwt import auth_required
from app.api.middlewares.cors import cors_middleware
from app.api.routers.auth import register_auth_routes
from app.api.routers.proxy import register_proxy_routes

app = Application()

app.middlewares.append(error_middleware)
app.middlewares.append(cors_middleware)
app.middlewares.append(auth_required)

@get("/health")
async def health():
    from app.core.config import settings
    return {"name": settings.APP_NAME, "status": "ok"}

register_auth_routes(app)
register_proxy_routes(app)
