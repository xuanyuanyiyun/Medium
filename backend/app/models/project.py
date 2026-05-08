from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ProjectType(str, Enum):
    VIDEO = "video"
    ARTICLE = "article"
    SHORT_VIDEO = "short_video"
    LIVE_STREAM = "live_stream"
    PODCAST = "podcast"
    SOCIAL_MEDIA = "social_media"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    project_type = Column(SQLEnum(ProjectType), nullable=False, default=ProjectType.VIDEO)
    status = Column(SQLEnum(ProjectStatus), nullable=False, default=ProjectStatus.DRAFT)
    
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True, index=True)
    
    metadata = Column(JSON, nullable=True)
    settings = Column(JSON, nullable=True)
    
    deadline = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", back_populates="projects")
    team = relationship("Team", back_populates="projects")
    topic = relationship("Topic", back_populates="projects")
    contents = relationship("Content", back_populates="project", cascade="all, delete-orphan")
    distributions = relationship("Distribution", back_populates="project", cascade="all, delete-orphan")
    analytics = relationship("Analytics", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, title='{self.title}', status='{self.status}')>"
