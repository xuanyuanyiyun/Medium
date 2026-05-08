import pytest
import asyncio
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
def mock_agent_input():
    from app.agents.base import AgentInput
    return AgentInput(
        task_id="test_task_001",
        params={},
        context={}
    )


@pytest.fixture
def mock_openai_response():
    return {
        "choices": [
            {
                "message": {
                    "content": "这是一篇测试文章的内容。AI技术正在快速发展，为内容创作带来新的可能性。"
                }
            }
        ]
    }


@pytest.fixture
def mock_dalle_response():
    return {
        "data": [
            {
                "url": "https://example.com/generated_image.png",
                "revised_prompt": "A professional article cover image"
            }
        ]
    }


@pytest.fixture
def mock_hot_topic_data():
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
        {
            "keyword": "内容创作方法论",
            "heat_score": 92.0,
            "source": "zhihu",
            "category": "education",
            "trend": "rising",
        },
        {
            "keyword": "短视频剪辑技巧",
            "heat_score": 88.3,
            "source": "douyin",
            "category": "entertainment",
            "trend": "stable",
        },
        {
            "keyword": "小红书爆款笔记",
            "heat_score": 90.1,
            "source": "xiaohongshu",
            "category": "lifestyle",
            "trend": "rising",
        },
    ]


@pytest.fixture
def mock_video_script_response():
    return """镜头1：开场画面
时长：5秒
台词：大家好，今天我们来聊聊AI技术

镜头2：技术展示
时长：10秒
台词：AI可以帮助我们完成很多事情

镜头3：案例分析
时长：15秒
台词：让我们看一个具体的例子

镜头4：总结
时长：5秒
台词：感谢观看，记得点赞关注"""

@pytest.fixture
def sample_article_params():
    return {
        "content_type": "article",
        "topic": "AI技术发展趋势",
        "outline": ["背景介绍", "技术现状", "未来展望"],
        "style": "professional",
    }


@pytest.fixture
def sample_video_params():
    return {
        "content_type": "video",
        "topic": "产品介绍视频",
        "duration": 60,
    }


@pytest.fixture
def sample_image_text_params():
    return {
        "content_type": "image_text",
        "topic": "端午节活动",
    }
