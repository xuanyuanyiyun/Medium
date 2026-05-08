from typing import Dict, Any, Optional
from datetime import datetime
import httpx
from app.platforms.base import PlatformAdapter


class WeChatAdapter(PlatformAdapter):
    def __init__(self):
        super().__init__("wechat")
        self.access_token: Optional[str] = None
        self.app_id: Optional[str] = None
        self.app_secret: Optional[str] = None

    async def authenticate(self, credentials: Dict[str, str]) -> bool:
        self.app_id = credentials.get("app_id")
        self.app_secret = credentials.get("app_secret")
        
        if not self.app_id or not self.app_secret:
            return False
        
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if "access_token" in data:
                self.access_token = data["access_token"]
                return True
        
        return False

    async def publish(
        self,
        title: str,
        content: str,
        cover_image_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        if not self.access_token:
            raise Exception("Not authenticated. Call authenticate() first.")

        url = "https://api.weixin.qq.com/cgi-bin/media/uploadnews"
        params = {"access_token": self.access_token}
        
        articles = [{
            "title": title,
            "thumb_media_id": kwargs.get("thumb_media_id", ""),
            "author": kwargs.get("author", ""),
            "digest": content[:54],
            "show_cover_pic": 1 if cover_image_url else 0,
            "content": content,
            "content_source_url": kwargs.get("source_url", ""),
        }]
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                params=params,
                json={"articles": articles},
            )
            data = response.json()
            
            if data.get("errcode", 0) == 0:
                return {
                    "success": True,
                    "post_id": data.get("media_id"),
                    "platform": "wechat",
                    "message": "发布成功",
                }
            else:
                return {
                    "success": False,
                    "error": data.get("errmsg", "Unknown error"),
                    "platform": "wechat",
                }

    async def get_post_status(self, post_id: str) -> Dict[str, Any]:
        return {
            "post_id": post_id,
            "status": "published",
            "url": f"https://mp.weixin.qq.com/s/{post_id}",
        }

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        return {
            "post_id": post_id,
            "read_count": 0,
            "like_count": 0,
            "comment_count": 0,
            "fetched_at": str(datetime.now()),
        }
