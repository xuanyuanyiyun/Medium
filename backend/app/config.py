"""应用配置管理"""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # 应用基本信息
    app_name: str = "媒体AI Agent工作流系统"
    app_version: str = "1.0.0"
    debug: bool = False

    # 数据库配置
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/media_agent"

    # API服务配置
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4

    # OpenAI配置
    openai_api_key: Optional[str] = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o"

    # Anthropic配置
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-sonnet-4-20250514"

    # 文件存储配置
    upload_dir: str = "./uploads"
    max_file_size: int = 100 * 1024 * 1024

    # JWT配置
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS配置
    cors_origins: list[str] = ["*"]

    # Redis配置（可选，用于缓存）
    redis_url: Optional[str] = None

    # Agent配置
    agent_max_iterations: int = 10
    agent_timeout: int = 300

    # 平台API配置
    douyin_client_key: Optional[str] = None
    douyin_client_secret: Optional[str] = None

    kuaishou_client_key: Optional[str] = None
    kuaishou_client_secret: Optional[str] = None

    xiaohongshu_client_key: Optional[str] = None
    xiaohongshu_client_secret: Optional[str] = None


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
