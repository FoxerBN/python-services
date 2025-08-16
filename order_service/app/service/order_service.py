from sqlalchemy.orm import Session
from app.model.order_model import Order
from app.schema.order_schema import OrderCreate
from app.util.check_stock_remote import check_stock_remote
from app.util.fetch_user import get_username_from_token
from app.util.decrease_stock_remote import decrease_stock_remote


async def get_all_my_orders(db: Session, token: str):
    """Get all orders for the current user"""
    user = get_username_from_token(token)
    if not user or not user["user_id"]:
        return {"error": "Invalid or expired token"}

    orders = db.query(Order).filter(Order.user_id == user["user_id"]).all()
    return orders


async def create_order(db: Session, order_data: OrderCreate, token: str):
    """Create a new order and decrease stock in stock-service."""
    user = get_username_from_token(token)
    if not user or not user["user_id"]:
        return {"error": "Invalid or expired token"}

    # Posielame rovno id (Pydantic aliasy v stock-service zvládnu aj item_id)
    items = [{"id": it.id, "amount": it.amount} for it in order_data.items]

    # Najprv overíme dostupnosť v stock-service
    try:
        stock_response = await check_stock_remote(items)
    except Exception as e:
        return {"error": f"Stock service nedostupný: {str(e)}"}

    if not stock_response["available"]:
        return stock_response

    # Vytvoríme objednávku v DB
    order = Order(
        user_id=user["user_id"],
        username=user["username"],
        items=[item.model_dump() for item in order_data.items],
        status="created"
    )
    db.add(order)

    # Znížime stav zásob
    decrease_result = await decrease_stock_remote(items)
    if not decrease_result.get("success"):
        db.rollback()
        return {"error": "Failed to decrease stock!"}

    db.commit()
    db.refresh(order)

    return {
        "success": True,
        "order_id": order.id,
        "user_id": user["user_id"],
        "username": user["username"]
    }


async def get_order_by_id(db: Session, order_id: int, token: str):
    """Retrieve a single order by its ID for the authenticated user."""
    user = get_username_from_token(token)
    if not user or not user["user_id"]:
        return {"error": "Invalid or expired token"}

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return {"error": "Order not found"}
    return order
