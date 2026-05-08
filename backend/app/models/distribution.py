from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Platform(str, Enum):
    WECHAT = "wechat"
    WECHAT_VIDEO = "wechat_video"
    WECHAT_MINI_PROGRAM = "wechat_mini_program"
    WEIBO = "weibo"
    DOUYIN = "douyin"
    KUAISHOU = "kuaishou"
    XIAOHONGSHU = "xiaohongshu"
    BILIBILI = "bilibili"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    ZHIHU = "zhihu"
    TOUTIAO = "toutiao"
    BAIDU = "baidu"


class DistributionStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"


class Distribution(Base):
    __tablename__ = "distributions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False, index=True)
    
    platform = Column(SQLEnum(Platform), nullable=False, index=True)
    status = Column(SQLEnum(DistributionStatus), nullable=False, default=DistributionStatus.PENDING)
    
    account_id = Column(String(255), nullable=True, index=True)
    channel_id = Column(String(255), nullable=True)
    
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    platform_post_id = Column(String(255), nullable=True, index=True)
    platform_url = Column(String(500), nullable=True)
    
    scheduled_time = Column(DateTime, nullable=True, index=True)
    published_at = Column(DateTime, nullable=True)
    
    metadata = Column(JSON, nullable=True)
    
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    is_auto_sync = Column(Boolean, default=False)
    sync_interval = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="distributions")
    content = relationship("Content", back_populates="distributions")
    platform_metrics = relationship("PlatformMetrics", back_populates="distribution", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Distribution(id={self.id}, platform='{self.platform}', status='{self.status}')>"


class PlatformMetrics(Base):
    __tablename__ = "platform_metrics"

    id = Column(Integer, primary_key=True, index=True)
    distribution_id = Column(Integer, ForeignKey("distributions.id"), nullable=False, index=True)
    
    platform = Column(String(100), nullable=False, index=True)
    metric_type = Column(String(50), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    
    follower_count = Column(Integer, nullable=True)
    engagement_rate = Column(Float, nullable=True)
    
    demographics = Column(JSON, nullable=True)
    data_points = Column(JSON, nullable=True)
    
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    fetched_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    distribution = relationship("Distribution", back_populates="platform_metrics")

    def __repr__(self):
        return f"<PlatformMetrics(id={self.id}, type='{self.metric_type}', value={self.metric_value})>"


class PlatformAccount(Base):
    __tablename__ = "platform_accounts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(SQLEnum(Platform), nullable=False, unique=True, index=True)
    
    account_name = Column(String(255), nullable=False)
    account_id = Column(String(255), nullable=False, unique=True)
    
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    
    permissions = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PlatformAccount(id={self.id}, platform='{self.platform}', account='{self.account_name}')>"
