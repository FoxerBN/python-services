from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func
from app.config.database import Base
from app.utils.verify_password import verify_password
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)
