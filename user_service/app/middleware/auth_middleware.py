from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.auth_tokens import decode_access_token

EXCLUDED_PATHS = {
    "/": {"GET"},
    "/api/v1/user/login": {"POST"},
    "/api/v1/user/add": {"POST"},
    "/api/v1/user/logout": {"POST"},
    "/healthz": {"GET"},
}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method

        if path in EXCLUDED_PATHS and method in EXCLUDED_PATHS[path]:
            return await call_next(request)

        token = request.cookies.get("access_token")
        if not token:
            return JSONResponse(status_code=401, content={"detail": "Missing token"})

        username = decode_access_token(token)
        if not username:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        request.state.username = username
        return await call_next(request)
