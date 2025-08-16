from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schema.order_schema import OrderCreate, OrderOut
from app.service.order_service import create_order, get_all_my_orders, get_order_by_id

router = APIRouter()

@router.post("/order")
async def create_order_route(
    order_data: OrderCreate,
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing token")

    result = await create_order(db, order_data, access_token)

    if "error" in result or (result.get("available") == False):
        raise HTTPException(status_code=400, detail=result)

    return result

@router.get("/order/me", response_model=List[OrderOut])
async def get_all_my_orders_route(
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing token")

    return await get_all_my_orders(db, access_token)

@router.get("/order/{order_id}", response_model=OrderOut)
async def get_order_by_id_route(
    order_id: int,
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing token")
    
    result = await get_order_by_id(db, order_id, access_token)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
