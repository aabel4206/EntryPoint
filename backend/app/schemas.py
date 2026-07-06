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

class SubscriptionCreate(BaseModel):
    profile_id: int
    resource_id: int


class SubscriptionResponse(BaseModel):
    subscription_id: int
    profile_id: int
    resource_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    notification_id: int
    profile_id: int
    resource_id: Optional[int] = None
    change_id: Optional[int] = None
    title: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class MonitoredPageCreate(BaseModel):
    resource_id: int
    category_id: int
    title: str
    url: str


class MonitoredPageResponse(BaseModel):
    page_id: int
    resource_id: int
    category_id: int
    title: str
    url: str
    last_content_hash: Optional[str] = None
    last_checked_at: Optional[datetime] = None
    active: bool

    class Config:
        from_attributes = True


class PageChangeLogResponse(BaseModel):
    change_id: int
    page_id: int
    previous_content_hash: Optional[str] = None
    new_content_hash: str
    change_summary: Optional[str] = None
    importance_level: str
    detected_at: datetime
    reviewed_by_admin: bool

    class Config:
        from_attributes = True