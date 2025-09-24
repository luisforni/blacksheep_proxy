from blacksheep import Request
from blacksheep.server.responses import Response
from app.core.config import settings

ALLOW_ORIGINS = settings.CORS_ALLOW_ORIGINS
ALLOW_HEADERS = settings.CORS_ALLOW_HEADERS
ALLOW_METHODS = settings.CORS_ALLOW_METHODS

async def cors_middleware(request: Request, handler):
    method = request.method.decode() if isinstance(request.method, (bytes, bytearray)) else request.method
    if method == "OPTIONS":
        return Response(200, [
            (b"access-control-allow-origin", ALLOW_ORIGINS.encode()),
            (b"access-control-allow-headers", ALLOW_HEADERS.encode()),
            (b"access-control-allow-methods", ALLOW_METHODS.encode()),
        ])
    response = await handler(request)
    response.add_header(b"access-control-allow-origin", ALLOW_ORIGINS.encode())
    response.add_header(b"access-control-allow-headers", ALLOW_HEADERS.encode())
    response.add_header(b"access-control-allow-methods", ALLOW_METHODS.encode())
    return response
