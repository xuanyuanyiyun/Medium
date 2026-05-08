from typing import Dict, Any, List, Optional
from datetime import datetime
import time
from app.agents.base import BaseAgent, AgentInput, AgentOutput
from app.services.llm_service import llm_service
from app.services.image_service import image_service


class CreationAgent(BaseAgent):
    def __init__(self):
        super().__init__("CreationAgent")
        self.llm_service = llm_service
        self.image_service = image_service

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        start_time = time.time()
        self.log_start(input_data)

        try:
            await self.validate_input(input_data)

            content_type = input_data.params.get("content_type", "article")
            
            if content_type == "article":
                result = await self.create_article(input_data)
            elif content_type == "video":
                result = await self.create_video_content(input_data)
            elif content_type == "image_text":
                result = await self.create_image_text(input_data)
            else:
                raise ValueError(f"Unsupported content type: {content_type}")

            execution_time = time.time() - start_time
            output = AgentOutput(
                success=True,
                data=result,
                execution_time=execution_time,
            )
            
            self.log_complete(input_data, output)
            return output

        except Exception as e:
            execution_time = time.time() - start_time
            output = AgentOutput(
                success=False,
                error=str(e),
                execution_time=execution_time,
            )
            self.log_complete(input_data, output)
            return output

    async def create_article(self, input_data: AgentInput) -> Dict[str, Any]:
        topic = input_data.params.get("topic", "")
        outline = input_data.params.get("outline", [])
        style = input_data.params.get("style", "professional")
        
        article = await self.llm_service.generate_article(topic, outline, style)
        
        if input_data.params.get("generate_cover", True):
            cover_url = await self.image_service.generate_cover_image(topic)
            article["cover_image_url"] = cover_url
        
        return article

    async def create_video_content(self, input_data: AgentInput) -> Dict[str, Any]:
        topic = input_data.params.get("topic", "")
        duration = input_data.params.get("duration", 60)
        
        script = await self.llm_service.generate_video_script(topic, duration)
        
        frames = []
        for i, shot in enumerate(script.get("shots", [])):
            frame_prompt = shot.get("description", "")
            if frame_prompt:
                try:
                    image_url = await self.image_service.generate_image(frame_prompt)
                    frames.append({
                        "shot_number": i + 1,
                        "description": shot.get("description", ""),
                        "dialogue": shot.get("dialogue", ""),
                        "duration": shot.get("duration", "5s"),
                        "image_url": image_url.get("url", ""),
                    })
                except Exception as e:
                    self.logger.warning(f"Failed to generate frame {i}: {e}")
        
        return {
            "topic": topic,
            "duration": duration,
            "script": script.get("script", ""),
            "shots": script.get("shots", []),
            "frames": frames,
        }

    async def create_image_text(self, input_data: AgentInput) -> Dict[str, Any]:
        topic = input_data.params.get("topic", "")
        
        prompt = f"Create an infographic about: {topic}. Include data visualization style."
        image_result = await self.image_service.generate_image(prompt, size="1792x1024")
        
        return {
            "topic": topic,
            "image_url": image_result.get("url", ""),
            "infographic_prompt": image_result.get("revised_prompt", ""),
        }
