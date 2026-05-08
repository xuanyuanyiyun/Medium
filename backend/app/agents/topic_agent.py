from typing import Dict, Any
from datetime import datetime
import time
from app.agents.base import BaseAgent, AgentInput, AgentOutput
from app.services.hot_topic_service import hot_topic_service


class TopicAgent(BaseAgent):
    def __init__(self):
        super().__init__("TopicAgent")
        self.hot_topic_service = hot_topic_service

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        start_time = time.time()
        self.log_start(input_data)

        try:
            await self.validate_input(input_data)

            action = input_data.params.get("action", "fetch_hot_topics")
            
            if action == "fetch_hot_topics":
                result = await self.fetch_hot_topics(input_data)
            elif action == "generate_topic_suggestions":
                result = await self.generate_topic_suggestions(input_data)
            elif action == "analyze_topic":
                result = await self.analyze_topic(input_data)
            else:
                result = {"error": f"Unknown action: {action}"}

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

    async def fetch_hot_topics(self, input_data: AgentInput) -> Dict[str, Any]:
        limit = input_data.params.get("limit", 20)
        category = input_data.params.get("category")
        region = input_data.params.get("region")
        
        topics = await self.hot_topic_service.fetch_all()
        
        if category:
            topics = [t for t in topics if t.get("category") == category]
        
        topics = topics[:limit]
        
        return {
            "topics": topics,
            "total": len(topics),
            "fetched_at": datetime.now().isoformat(),
        }

    async def generate_topic_suggestions(self, input_data: AgentInput) -> Dict[str, Any]:
        keyword = input_data.params.get("keyword")
        
        suggestions = [
            {
                "title": f"{keyword}的深度解析",
                "angle": "深度分析",
                "outline": ["背景介绍", "核心问题", "解决方案", "总结展望"],
            },
            {
                "title": f"{keyword}实用指南",
                "angle": "实用教程",
                "outline": ["基础概念", "操作步骤", "注意事项", "案例分享"],
            },
            {
                "title": f"{keyword}行业观察",
                "angle": "行业视角",
                "outline": ["行业现状", "发展趋势", "竞争格局", "投资机会"],
            },
        ]
        
        return {
            "keyword": keyword,
            "suggestions": suggestions,
        }

    async def analyze_topic(self, input_data: AgentInput) -> Dict[str, Any]:
        topic = input_data.params.get("topic", "")
        
        return {
            "topic": topic,
            "heat_level": "high",
            "competition_level": "medium",
            "audience": "25-35岁职场人群",
            "best_publish_time": "工作日午休时间 12:00-13:30",
            "related_keywords": [f"{topic}技巧", f"{topic}方法", f"{topic}案例"],
        }
