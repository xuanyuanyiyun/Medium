from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PlatformAdapter(ABC):
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.logger = logging.getLogger(f"{__name__}.{platform_name}")

    @abstractmethod
    async def authenticate(self, credentials: Dict[str, str]) -> bool:
        pass

    @abstractmethod
    async def publish(
        self,
        title: str,
        content: str,
        cover_image_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_post_status(self, post_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        pass

    async def adapt_content(
        self,
        content: str,
        platform: str,
        max_length: Optional[int] = None,
    ) -> str:
        if max_length and len(content) > max_length:
            return content[:max_length] + "..."
        return content

    async def generate_caption(
        self,
        title: str,
        content: str,
        platform: str,
    ) -> str:
        return f"{title}\n\n{content[:200]}..."


class PlatformManager:
    def __init__(self):
        self._adapters: Dict[str, PlatformAdapter] = {}

    def register(self, platform: str, adapter: PlatformAdapter):
        self._adapters[platform] = adapter

    def get_adapter(self, platform: str) -> Optional[PlatformAdapter]:
        return self._adapters.get(platform)

    def list_platforms(self) -> list:
        return list(self._adapters.keys())


platform_manager = PlatformManager()
