from typing import List, Dict, Any, Optional
import asyncio
import httpx
from datetime import datetime


class HotTopicService:
    def __init__(self):
        self.platforms = ["weibo", "zhihu", "douyin", "xiaohongshu"]

    async def fetch_weibo_hot(self) -> List[Dict[str, Any]]:
        return [
            {
                "keyword": "AI技术突破",
                "heat_score": 98.5,
                "source": "weibo",
                "category": "technology",
                "trend": "rising",
            },
            {
                "keyword": "新媒体运营技巧",
                "heat_score": 85.2,
                "source": "weibo",
                "category": "business",
                "trend": "stable",
            },
        ]

    async def fetch_zhihu_hot(self) -> List[Dict[str, Any]]:
        return [
            {
                "keyword": "内容创作方法论",
                "heat_score": 92.0,
                "source": "zhihu",
                "category": "education",
                "trend": "rising",
            },
        ]

    async def fetch_douyin_trending(self) -> List[Dict[str, Any]]:
        return [
            {
                "keyword": "短视频剪辑技巧",
                "heat_score": 88.3,
                "source": "douyin",
                "category": "entertainment",
                "trend": "stable",
            },
        ]

    async def fetch_xiaohongshu_trending(self) -> List[Dict[str, Any]]:
        return [
            {
                "keyword": "小红书爆款笔记",
                "heat_score": 90.1,
                "source": "xiaohongshu",
                "category": "lifestyle",
                "trend": "rising",
            },
        ]

    async def fetch_all(self) -> List[Dict[str, Any]]:
        all_topics = []
        
        async with httpx.AsyncClient() as client:
            weibo_tasks = self.fetch_weibo_hot()
            zhihu_tasks = self.fetch_zhihu_hot()
            douyin_tasks = self.fetch_douyin_trending()
            xhs_tasks = self.fetch_xiaohongshu_trending()
            
            results = await asyncio.gather(
                weibo_tasks, zhihu_tasks, douyin_tasks, xhs_tasks
            )
            
            for topics in results:
                all_topics.extend(topics)
        
        return sorted(all_topics, key=lambda x: x["heat_score"], reverse=True)


hot_topic_service = HotTopicService()
