from typing import Optional, List, Dict, Any
import httpx
import os


class ImageService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.dalle_endpoint = "https://api.openai.com/v1/images/generations"

    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.dalle_endpoint,
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "dall-e-3",
                    "prompt": prompt,
                    "size": size,
                    "quality": quality,
                    "n": 1,
                },
                timeout=60.0,
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "url": data["data"][0]["url"],
                    "revised_prompt": data["data"][0].get("revised_prompt", ""),
                }
            else:
                raise Exception(f"Image generation failed: {response.text}")

    async def generate_cover_image(
        self,
        title: str,
        style: str = "modern and clean",
    ) -> str:
        prompt = f"A professional article cover image for: {title}. Style: {style}"
        result = await self.generate_image(prompt)
        return result["url"]

    async def generate_video_thumbnail(
        self,
        topic: str,
        style: str = "cinematic and eye-catching",
    ) -> str:
        prompt = f"A video thumbnail for: {topic}. Style: {style}, text overlay friendly"
        result = await self.generate_image(prompt, size="1792x1024")
        return result["url"]


image_service = ImageService()
