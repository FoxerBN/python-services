import logging
from sqlalchemy.orm import Session
from app.model.stock_model import StockItem
from app.schema.stock_check_schema import CheckItem, CheckStockResponse, MissingItem
from app.schema.stock_schema import DecreaseItem, StockItemCreate

logger = logging.getLogger(__name__)


def get_item_by_id(id: int, db: Session) -> StockItem | None:
    """Get a stock item by its ID.
    Args:
        id (int): The ID of the stock item to retrieve.
        db (Session): The database session.

    Returns:
        StockItem | None: The stock item if found, otherwise None.
    """
    return db.query(StockItem).filter(StockItem.id == id).first()

def get_all_by_category(category: str, db: Session) -> list[StockItem]:
    """Get all stock items by category.
    Args:
        category (str): The category of the stock items to retrieve.
        db (Session): The database session.

    Returns:
        list[StockItem]: The list of stock items in the specified category.
    """
    return db.query(StockItem).filter(StockItem.category == category).all()


def get_all_items(db: Session) -> list[StockItem]:
    """Get all stock items.
    Args:
        db (Session): The database session.

    Returns:
        list[StockItem]: The list of all stock items.
    """
    return db.query(StockItem).all()


def check_stock_availability(items: list[CheckItem], db: Session) -> CheckStockResponse:
    """Check availability.
    Args:
        items (list[CheckItem]): The list of items to check.
        db (Session): The database session.

    Returns:
        CheckStockResponse: The response containing the availability status and missing items.
    """
    missing = []
    for req_item in items:
        stock = db.query(StockItem).filter(StockItem.id == req_item.id).first()
        if not stock or stock.amount < req_item.amount:
            missing.append(MissingItem(
                id=req_item.id,
                requested=req_item.amount,
                available=stock.amount if stock else 0
            ))
    return CheckStockResponse(
        available=len(missing) == 0,
        missing=missing
    )



def decrease_stock(items: list[DecreaseItem], db: Session) -> dict:
    """Decrease stock items by id and amount.
    Returns a dictionary with success status, decreased item ids, and not found item ids.
    """
    decreased = []
    not_found = []
    for req_item in items:
        stock = db.query(StockItem).filter(StockItem.id == req_item.id).first()
        if stock and stock.amount >= req_item.amount:
            stock.amount -= req_item.amount
            decreased.append(req_item.id)
        else:
            not_found.append(req_item.id)
    db.commit()
    return {"success": len(not_found) == 0, "decreased": decreased, "not_found": not_found}


def increase_one_stock(id: int, name: str, category: str, amount: int, db: Session) -> dict:
    """Update a single stock item by id. Sets name, category, and amount.
    Logs an error if the item does not exist.
    """
    stock = db.query(StockItem).filter(StockItem.id == id).first()
    if not stock:
        logger.error("Item not found: id=%s, name=%s, category=%s", id, name, category)
        return {"success": False, "error": "Item not found"}

    stock.name = name
    stock.category = category
    stock.amount = amount
    db.commit()
    db.refresh(stock)
    return {
        "success": True,
        "id": stock.id,
        "category": stock.category,
        "name": stock.name,
        "amount": stock.amount,
    }


def create_stock_item(item_data: StockItemCreate, db: Session) -> StockItem:
    """Create a new stock item.
    Args:
        item_data (StockItemCreate): The stock item data to create.
        db (Session): The database session.

    Returns:
        StockItem: The created stock item.
    """
    new_item = StockItem(
        category=item_data.category,
        name=item_data.name,
        amount=item_data.amount
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


