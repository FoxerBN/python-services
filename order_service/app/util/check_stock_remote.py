import httpx
import os

STOCK_SERVICE_CHECK = os.getenv(
    "STOCK_SERVICE_CHECK",
    "http://localhost:9990/api/v1/stock/check"
)
async def check_stock_remote(items: list[dict]) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(STOCK_SERVICE_CHECK, json={"items": items})
        resp.raise_for_status()
        return resp.json()