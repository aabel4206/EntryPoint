from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ResourceCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class ResourceCategoryCreate(ResourceCategoryBase):
    pass


class ResourceCategoryResponse(ResourceCategoryBase):
    category_id: int

    class Config:
        from_attributes = True


class ResourceBase(BaseModel):
    category_id: int
    title: str
    description: Optional[str] = None
    url: str


class ResourceCreate(ResourceBase):
    pass


class ResourceResponse(ResourceBase):
    resource_id: int
    last_reviewed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True