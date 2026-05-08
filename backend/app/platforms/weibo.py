from typing import Dict, Any, Optional
import httpx
from app.platforms.base import PlatformAdapter


class WeiboAdapter(PlatformAdapter):
    def __init__(self):
        super().__init__("weibo")
        self.access_token: Optional[str] = None
        self.client_id: Optional[str] = None
        self.client_secret: Optional[str] = None

    async def authenticate(self, credentials: Dict[str, str]) -> bool:
        self.client_id = credentials.get("client_id")
        self.client_secret = credentials.get("client_secret")
        
        return bool(self.client_id and self.client_secret)

    async def publish(
        self,
        title: str,
        content: str,
        cover_image_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        if not self.access_token:
            return {
                "success": False,
                "error": "Not authenticated",
                "platform": "weibo",
            }

        url = "https://api.weibo.com/2/statuses/share.json"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        post_content = f"{title} {content}"
        if cover_image_url:
            post_content += f" {cover_image_url}"
        
        data = {
            "status": post_content[:2000],
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                data=data,
            )
            result = response.json()
            
            if "idstr" in result:
                return {
                    "success": True,
                    "post_id": result["idstr"],
                    "platform": "weibo",
                    "url": f"https://weibo.com/{result['idstr']}",
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                    "platform": "weibo",
                }

    async def get_post_status(self, post_id: str) -> Dict[str, Any]:
        return {
            "post_id": post_id,
            "status": "published",
        }

    async def get_analytics(self, post_id: str) -> Dict[str, Any]:
        return {
            "post_id": post_id,
            "reposts": 0,
            "comments": 0,
            "attitudes": 0,
        }
