from typing import Optional

from pydantic import BaseModel, ConfigDict

class BaseUserCategory(BaseModel):
    id: int
    user_id: int
    category_id: int
    custom_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class BaseUserCategoryCreate(BaseModel):
    category_id: int
    custom_name: Optional[str] = None


class BaseUserCategoryUpdate(BaseModel):
    custom_name: Optional[str] = None
