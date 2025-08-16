from pydantic import BaseModel, Field, AliasChoices, ConfigDict
from typing import List

class CheckItem(BaseModel):
    # prijme buď "item_id" alebo "id", interne to bude "id"
    id: int = Field(validation_alias=AliasChoices("item_id", "id"))
    amount: int
    model_config = ConfigDict(populate_by_name=True)

class CheckStockRequest(BaseModel):
    items: List[CheckItem]

class MissingItem(BaseModel):
    id: int
    requested: int
    available: int

class CheckStockResponse(BaseModel):
    available: bool
    missing: List[MissingItem] = []
