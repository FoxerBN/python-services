import httpx
import os

STOCK_SERVICE_DECREASE = os.getenv(
    "STOCK_SERVICE_DECREASE",
    "http://localhost:9990/api/v1/stock/decrease"
)
async def decrease_stock_remote(items: list[dict]) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(STOCK_SERVICE_DECREASE, json={"items": items})
        resp.raise_for_status()
        return resp.json()