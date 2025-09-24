from blacksheep import Request
from blacksheep.server.responses import json
from app.core.security import decode_token

BEARER = "bearer"

async def auth_required(request: Request, handler):
    path = request.url.path.decode()
    if path.startswith("/auth/") or path == "/health" or path.startswith("/_debug"):
        return await handler(request)

    auth = request.headers.get_first(b"authorization")
    if not auth:
        return json({"error": "Missing Authorization"}, status=401)

    parts = auth.decode().split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != BEARER:
        return json({"error": "Invalid Authorization header"}, status=401)

    token = parts[1].strip()
    try:
        decode_token(token) 
    except Exception:
        return json({"error": "Invalid or expired token"}, status=401)

    return await handler(request)
