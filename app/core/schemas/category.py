from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseCategory(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class BaseCategoryCreate(BaseModel):
    name: str


class BaseCategoryUpdate(BaseModel):
    name: Optional[str] = None
