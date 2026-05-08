from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    WECHAT = "wechat"
    WEIBO = "weibo"
    ZHIHU = "zhihu"
    XIAOHONGSHU = "xiaohongshu"
    DOUYIN = "douyin"
    KUAISHOU = "kuaishou"
    BILIBILI = "bilibili"
    TOUTIAO = "toutiao"


class DistributionStatus(str, Enum):
    PENDING = "pending"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"


class DistributionCreate(BaseModel):
    project_id: int
    content_id: Optional[int] = None
    platforms: List[Platform]
    scheduled_time: Optional[datetime] = None
    title: Optional[str] = None
    adapted_content: Optional[str] = None
    cover_image_url: Optional[str] = None


class DistributionUpdate(BaseModel):
    status: Optional[DistributionStatus] = None
    platform_post_id: Optional[str] = None
    platform_post_url: Optional[str] = None


class DistributionResponse(BaseModel):
    id: int
    project_id: int
    content_id: Optional[int]
    platform: Platform
    status: DistributionStatus
    title: Optional[str]
    adapted_content: Optional[str]
    cover_image_url: Optional[str]
    platform_post_id: Optional[str]
    platform_post_url: Optional[str]
    scheduled_time: Optional[datetime]
    published_at: Optional[datetime]
    error_message: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
