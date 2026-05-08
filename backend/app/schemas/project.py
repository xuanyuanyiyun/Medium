from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ProjectType(str, Enum):
    ARTICLE = "article"
    VIDEO = "video"
    IMAGE_TEXT = "image_text"


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    TOPIC_SELECTING = "topic_selecting"
    CREATING = "creating"
    REVIEWING = "reviewing"
    PENDING_DISTRIBUTION = "pending_distribution"
    DISTRIBUTING = "distributing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: ProjectType
    workflow_mode: str = "professional"
    config: Dict[str, Any] = {}


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[ProjectStatus] = None
    config: Optional[Dict[str, Any]] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    type: ProjectType
    status: ProjectStatus
    workflow_mode: str
    config: Dict[str, Any]
    result: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
    total: int
    page: int
    page_size: int
