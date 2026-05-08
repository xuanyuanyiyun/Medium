from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from app.database import Base


class ContentType(str, Enum):
    VIDEO = "video"
    ARTICLE = "article"
    SHORT_VIDEO = "short_video"
    IMAGE = "image"
    AUDIO = "audio"
    DOCUMENT = "document"
    POST = "post"


class ContentStatus(str, Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    GENERATED = "generated"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    content_type = Column(SQLEnum(ContentType), nullable=False)
    status = Column(SQLEnum(ContentStatus), nullable=False, default=ContentStatus.DRAFT)
    
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    body = Column(Text, nullable=True)
    
    url = Column(String(500), nullable=True)
    file_path = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    
    metadata = Column(JSON, nullable=True)
    
    duration = Column(Float, nullable=True)
    word_count = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)
    
    version = Column(Integer, nullable=False, default=1)
    parent_content_id = Column(Integer, ForeignKey("contents.id"), nullable=True)
    
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="contents")
    parent_content = relationship("Content", remote_side=[id], backref="revisions")
    assets = relationship("Asset", back_populates="content", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Content(id={self.id}, type='{self.content_type}', status='{self.status}')>"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False, index=True)
    
    asset_type = Column(String(50), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_url = Column(String(500), nullable=True)
    
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)
    
    metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    content = relationship("Content", back_populates="assets")

    def __repr__(self):
        return f"<Asset(id={self.id}, type='{self.asset_type}', file_name='{self.file_name}')>"
