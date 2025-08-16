# app/schema/order_schema.py
from pydantic import BaseModel, Field, AliasChoices, ConfigDict
from datetime import datetime
from typing import List

class OrderItem(BaseModel):
    # prijme "id" aj historické "item_id"
    id: int = Field(validation_alias=AliasChoices("id", "item_id"))
    amount: int
    # ak by si niekde serializovala späť s "id", povolí populate_by_name
    model_config = ConfigDict(populate_by_name=True)

class OrderCreate(BaseModel):
    items: List[OrderItem]

class OrderOut(BaseModel):
    id: int
    user_id: int
    username: str
    items: List[OrderItem]
    status: str
    created_at: datetime
    # Pydantic v2: namiesto Config.orm_mode = True
    model_config = ConfigDict(from_attributes=True)
