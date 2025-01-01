from typing import Optional

from pydantic import BaseModel, ConfigDict

class BaseCategory(BaseModel):
    id: int
    name: str
    is_default: bool

    model_config = ConfigDict(from_attributes=True)


class BaseCategoryCreate(BaseModel):
    name: str
    is_default: Optional[bool] = False


class BaseCategoryUpdate(BaseModel):
    name: Optional[str] = None
    is_default: Optional[bool] = None
