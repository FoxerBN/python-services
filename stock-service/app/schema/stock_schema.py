from pydantic import BaseModel, Field, AliasChoices, ConfigDict
from typing import List

class StockItemBase(BaseModel):
    category: str
    name: str
    amount: int

class StockItemCreate(StockItemBase):
    pass

class StockItemUpdate(StockItemBase):
    id: int

class DecreaseItem(BaseModel):
    # opäť prijme "item_id" aj "id", interne používa "id"
    id: int = Field(validation_alias=AliasChoices("item_id", "id"))
    amount: int
    model_config = ConfigDict(populate_by_name=True)

class DecreaseStockRequest(BaseModel):
    items: List[DecreaseItem]

class StockItemOut(StockItemBase):
    id: int
    class Config:
        orm_mode = True
