from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class AnalyticsEventType(str, Enum):
    PAGE_VIEW = "page_view"
    CONTENT_VIEW = "content_view"
    VIDEO_PLAY = "video_play"
    VIDEO_COMPLETE = "video_complete"
    LIKE = "like"
    SHARE = "share"
    COMMENT = "comment"
    SUBSCRIBE = "subscribe"
    DOWNLOAD = "download"
    CTA_CLICK = "cta_click"


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    event_type = Column(String(50), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    session_id = Column(String(255), nullable=True, index=True)
    
    platform = Column(String(100), nullable=True, index=True)
    device_type = Column(String(50), nullable=True)
    browser = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    
    referrer = Column(String(500), nullable=True)
    utm_source = Column(String(255), nullable=True)
    utm_medium = Column(String(255), nullable=True)
    utm_campaign = Column(String(255), nullable=True)
    
    duration = Column(Float, nullable=True)
    scroll_depth = Column(Float, nullable=True)
    
    metadata = Column(JSON, nullable=True)
    properties = Column(JSON, nullable=True)
    
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    project = relationship("Project", back_populates="analytics")

    def __repr__(self):
        return f"<Analytics(id={self.id}, event='{self.event_type}', created='{self.created_at}')>"


class ContentPerformance(Base):
    __tablename__ = "content_performance"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    date = Column(DateTime, nullable=False, index=True)
    
    total_views = Column(Integer, default=0)
    unique_views = Column(Integer, default=0)
    total_plays = Column(Integer, default=0)
    complete_plays = Column(Integer, default=0)
    
    total_likes = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    total_saves = Column(Integer, default=0)
    
    engagement_rate = Column(Float, nullable=True)
    completion_rate = Column(Float, nullable=True)
    avg_watch_time = Column(Float, nullable=True)
    
    click_through_rate = Column(Float, nullable=True)
    conversion_rate = Column(Float, nullable=True)
    
    revenue = Column(Float, default=0)
    cost = Column(Float, default=0)
    roi = Column(Float, nullable=True)
    
    platform_breakdown = Column(JSON, nullable=True)
    demographic_breakdown = Column(JSON, nullable=True)
    geographic_breakdown = Column(JSON, nullable=True)
    
    metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ContentPerformance(id={self.id}, date='{self.date}', views={self.total_views})>"


class DailyMetrics(Base):
    __tablename__ = "daily_metrics"

    id = Column(Integer, primary_key=True, index=True)
    
    date = Column(DateTime, nullable=False, unique=True, index=True)
    period_type = Column(String(50), nullable=False)
    
    total_projects = Column(Integer, default=0)
    active_projects = Column(Integer, default=0)
    published_content = Column(Integer, default=0)
    
    total_views = Column(Integer, default=0)
    total_engagements = Column(Integer, default=0)
    total_followers = Column(Integer, default=0)
    follower_growth = Column(Integer, default=0)
    
    top_performing_content = Column(JSON, nullable=True)
    platform_breakdown = Column(JSON, nullable=True)
    content_type_breakdown = Column(JSON, nullable=True)
    
    ai_generation_stats = Column(JSON, nullable=True)
    distribution_stats = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<DailyMetrics(id={self.id}, date='{self.date}')>"


class ReportTemplate(Base):
    __tablename__ = "report_templates"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    report_type = Column(String(50), nullable=False)
    
    template_config = Column(JSON, nullable=False)
    
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ReportTemplate(id={self.id}, name='{self.name}', type='{self.report_type}')>"
