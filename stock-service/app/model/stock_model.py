from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.config.database import Base

class StockItem(Base):
    __tablename__ = "stock_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False, default=0)
