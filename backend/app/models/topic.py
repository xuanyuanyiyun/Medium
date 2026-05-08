from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class TrendStatus(str, Enum):
    EMERGING = "emerging"
    RISING = "rising"
    PEAKING = "peaking"
    DECLINING = "declining"
    STABLE = "stable"


class TopicSource(str, Enum):
    TRENDING = "trending"
    BREAKING = "breaking"
    SCHEDULED = "scheduled"
    RECOMMENDED = "recommended"
    MANUAL = "manual"


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    source = Column(SQLEnum(TopicSource), nullable=False, default=TopicSource.RECOMMENDED)
    
    category = Column(String(100), nullable=True, index=True)
    tags = Column(JSON, nullable=True)
    keywords = Column(JSON, nullable=True)
    
    trend_status = Column(SQLEnum(TrendStatus), nullable=True)
    trend_score = Column(Float, nullable=True)
    engagement_score = Column(Float, nullable=True)
    
    source_url = Column(String(500), nullable=True)
    source_platform = Column(String(100), nullable=True)
    original_author = Column(String(255), nullable=True)
    
    is_trending = Column(Boolean, default=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    is_priority = Column(Boolean, default=False)
    
    scheduled_date = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    metadata = Column(JSON, nullable=True)
    
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True, index=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", back_populates="topics")
    team = relationship("Team", back_populates="topics")
    projects = relationship("Project", back_populates="topic")
    trend_data = relationship("TopicTrendData", back_populates="topic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Topic(id={self.id}, title='{self.title}', status='{self.trend_status}')>"


class TopicTrendData(Base):
    __tablename__ = "topic_trend_data"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)
    
    platform = Column(String(100), nullable=False, index=True)
    metric_type = Column(String(50), nullable=False)
    metric_value = Column(Float, nullable=False)
    
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)

    topic = relationship("Topic", back_populates="trend_data")

    def __repr__(self):
        return f"<TopicTrendData(id={self.id}, platform='{self.platform}', metric='{self.metric_type}')>"
