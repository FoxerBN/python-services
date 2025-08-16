from fastapi import FastAPI
from app.config.database import Base, engine
from app.api.v1 import stock_route
from app.middleware.logger_middleware import logger_middleware

app = FastAPI(
    title="Stock Service API",
    description="A simple stock management service",
    version="1.0.0"
)

# DB init
Base.metadata.create_all(bind=engine)

# Middleware
app.middleware("http")(logger_middleware)

# Healthcheck pre Docker
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# Root (len info)
@app.get("/")
def root():
    return {"message": "Stock service is running!"}

# API routy
app.include_router(
    stock_route.router,
    prefix="/api/v1",
    tags=["Stock"]
)
