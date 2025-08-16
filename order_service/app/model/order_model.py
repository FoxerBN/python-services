from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, JSON, func
from app.config.database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    items: Mapped[list] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
