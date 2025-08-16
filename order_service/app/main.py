from fastapi import FastAPI
from app.config.database import Base, engine
from app.api.v1.order_route import router as order_router
from app.middleware.logger_middleware import logger_middleware

app = FastAPI(
    title="Order Service API",
    description="A simple order management service",
    version="1.0.0",
)

# DB init (SQLite tabuľky)
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
    return {"message": "Order service is running!"}

# API routy
app.include_router(
    order_router,
    prefix="/api/v1",
    tags=["Order"]
)
