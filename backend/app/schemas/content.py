from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ContentType(str, Enum):
    ARTICLE = "article"
    VIDEO = "video"
    IMAGE_TEXT = "image_text"


class ContentStatus(str, Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ContentCreate(BaseModel):
    project_id: int
    type: ContentType
    title: Optional[str] = None
    body: Optional[str] = None
    outline: Optional[Dict[str, Any]] = None


class ContentUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    outline: Optional[Dict[str, Any]] = None
    media_urls: Optional[List[str]] = None


class ContentResponse(BaseModel):
    id: int
    project_id: int
    type: ContentType
    title: Optional[str]
    body: Optional[str]
    outline: Optional[Dict[str, Any]]
    media_urls: List[str]
    metadata: Dict[str, Any]
    status: ContentStatus
    error_message: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
