from fastapi import Request
from app.util.logger import get_logger
import time

logger = get_logger()

async def logger_middleware(request: Request, call_next):
    start_time = time.time()
    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    logger.info(f"Request: {request.method} {request.url.path}")
    logger.info(f"IP: {ip}")
    logger.info(f"User-Agent: {user_agent}")

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000  # ms
    logger.info(f"Response status: {request.method} {request.url.path}")
    logger.info(f"Processing time: {process_time:.2f} ms")
    logger.info(f"Response: {response.status_code}")
    logger.info("-" * 40)

    return response
