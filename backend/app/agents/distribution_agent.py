from typing import Dict, Any, List, Optional
from datetime import datetime
import time
from app.agents.base import BaseAgent, AgentInput, AgentOutput
from app.platforms.wechat import WeChatAdapter
from app.platforms.weibo import WeiboAdapter
from app.platforms.base import platform_manager


class DistributionAgent(BaseAgent):
    def __init__(self):
        super().__init__("DistributionAgent")
        self._register_platforms()

    def _register_platforms(self):
        wechat_adapter = WeChatAdapter()
        weibo_adapter = WeiboAdapter()
        
        platform_manager.register("wechat", wechat_adapter)
        platform_manager.register("weibo", weibo_adapter)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        start_time = time.time()
        self.log_start(input_data)

        try:
            await self.validate_input(input_data)

            action = input_data.params.get("action", "publish")
            
            if action == "publish":
                result = await self.publish_to_platforms(input_data)
            elif action == "adapt_content":
                result = await self.adapt_content_for_platform(input_data)
            elif action == "schedule":
                result = await self.schedule_publication(input_data)
            elif action == "get_status":
                result = await self.get_distribution_status(input_data)
            else:
                raise ValueError(f"Unknown action: {action}")

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

    async def publish_to_platforms(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        platforms = input_data.params.get("platforms", [])
        title = input_data.params.get("title", "")
        content = input_data.params.get("content", "")
        cover_image_url = input_data.params.get("cover_image_url")
        credentials = input_data.params.get("credentials", {})
        
        results = []
        
        for platform_name in platforms:
            adapter = platform_manager.get_adapter(platform_name)
            
            if not adapter:
                results.append({
                    "platform": platform_name,
                    "success": False,
                    "error": "Platform not supported",
                })
                continue
            
            platform_creds = credentials.get(platform_name, {})
            auth_result = await adapter.authenticate(platform_creds)
            
            if not auth_result:
                results.append({
                    "platform": platform_name,
                    "success": False,
                    "error": "Authentication failed",
                })
                continue
            
            try:
                adapted_content = await adapter.adapt_content(
                    content,
                    platform_name,
                    max_length=2000 if platform_name == "weibo" else None,
                )
                
                publish_result = await adapter.publish(
                    title=title,
                    content=adapted_content,
                    cover_image_url=cover_image_url,
                )
                
                results.append({
                    "platform": platform_name,
                    **publish_result,
                })
                
            except Exception as e:
                results.append({
                    "platform": platform_name,
                    "success": False,
                    "error": str(e),
                })
        
        successful = sum(1 for r in results if r.get("success", False))
        
        return {
            "total": len(results),
            "successful": successful,
            "failed": len(results) - successful,
            "results": results,
            "distributed_at": datetime.now().isoformat(),
        }

    async def adapt_content_for_platform(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        platform = input_data.params.get("platform")
        title = input_data.params.get("title", "")
        content = input_data.params.get("content", "")
        
        adapter = platform_manager.get_adapter(platform)
        
        if not adapter:
            raise ValueError(f"Platform not supported: {platform}")
        
        adapted = await adapter.adapt_content(content, platform)
        caption = await adapter.generate_caption(title, content, platform)
        
        return {
            "platform": platform,
            "adapted_content": adapted,
            "caption": caption,
        }

    async def schedule_publication(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        platforms = input_data.params.get("platforms", [])
        scheduled_time = input_data.params.get("scheduled_time")
        
        return {
            "scheduled": True,
            "platforms": platforms,
            "scheduled_time": scheduled_time,
            "message": "定时发布任务已创建",
        }

    async def get_distribution_status(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        distribution_id = input_data.params.get("distribution_id")
        platform = input_data.params.get("platform")
        post_id = input_data.params.get("post_id")
        
        adapter = platform_manager.get_adapter(platform)
        
        if not adapter:
            raise ValueError(f"Platform not supported: {platform}")
        
        status = await adapter.get_post_status(post_id)
        
        return {
            "distribution_id": distribution_id,
            "platform": platform,
            **status,
        }
