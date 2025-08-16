from fastapi import FastAPI
from app.config.database import Base, engine
from app.api.v1 import user_routes, auth_routes
from app.middleware.logger_middleware import logger_middleware
from app.middleware.auth_middleware import AuthMiddleware

app = FastAPI(
    title="User Service API",
    description="A simple user management service",
    version="1.0.0"
)

# DB init
Base.metadata.create_all(bind=engine)

# Middleware
app.middleware("http")(logger_middleware)
app.add_middleware(AuthMiddleware)

# Healthcheck pre Docker
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# Root (len info)
@app.get("/")
def root():
    return {"message": "User service is running!"}

# API routy
app.include_router(
    user_routes.router,
    prefix="/api/v1",
    tags=["Users"]
)
app.include_router(
    auth_routes.router,
    prefix="/api/v1",
    tags=["Authentication"]
)
