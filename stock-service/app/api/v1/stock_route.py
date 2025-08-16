from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.service.stock_service import (
    get_item_by_id,
    get_all_by_category,
    get_all_items,
    check_stock_availability,
    decrease_stock,
    increase_one_stock,
    create_stock_item
)
from app.schema.stock_check_schema import CheckStockRequest, CheckStockResponse
from app.config.database import get_db
from app.schema.stock_schema import StockItemOut, DecreaseStockRequest, StockItemUpdate, StockItemCreate
router = APIRouter()

@router.get("/stock/one/{id}", response_model=StockItemOut)
def get_stock_item(id: int, db: Session = Depends(get_db)):
    item = get_item_by_id(id, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/stock", response_model=list[StockItemOut])
def get_stock_items_by_category(category: str = Query(...), db: Session = Depends(get_db)):
    items = get_all_by_category(category, db)
    if not items:
        raise HTTPException(status_code=404, detail="No items found in the specified category")
    return items


@router.get("/stock/all", response_model=list[StockItemOut])
def get_all_stock_items(db: Session = Depends(get_db)):
    items = get_all_items(db)
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items


@router.post("/stock/check", response_model=CheckStockResponse)
def check_stock_route(
    body: CheckStockRequest,
    db: Session = Depends(get_db)
):
    result = check_stock_availability(body.items, db)
    return result

@router.post("/stock/decrease")
def decrease_stock_route(
    body: DecreaseStockRequest,
    db: Session = Depends(get_db)
):
    result = decrease_stock(body.items, db)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/stock/increase-one")
def increase_one_stock_route(
    body: StockItemUpdate,
    db: Session = Depends(get_db)
):
    result = increase_one_stock(body.id, body.name, body.category, body.amount, db)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.post("/stock/create", response_model=StockItemOut)
def create_stock_route(
    body: StockItemCreate,
    db: Session = Depends(get_db)
):
    item = create_stock_item(body, db)
    return item
