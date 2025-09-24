from blacksheep import json
from app.schemas.auth import LoginIn, TokenOut
from app.core.security import create_access_token, verify_password, hash_password

FAKE_USERS = {"admin@example.com": hash_password("admin123")}

def register_auth_routes(app):
    @app.router.post("/auth/token")
    async def login(data: LoginIn):
        hashed = FAKE_USERS.get(data.username)
        if not hashed or not verify_password(data.password, hashed):
            return json({"error": "Invalid credentials"}, status=401)
        token = create_access_token(sub=data.username, claims={"roles": ["admin"]})
        return json(TokenOut(access_token=token).model_dump())
