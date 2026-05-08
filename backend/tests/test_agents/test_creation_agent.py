import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from app.agents.creation_agent import CreationAgent
from app.agents.base import AgentInput, AgentOutput


@pytest.fixture
def creation_agent():
    return CreationAgent()


@pytest.fixture
def mock_llm_service():
    mock_service = MagicMock()
    mock_service.generate_article = AsyncMock(return_value={
        "title": "测试文章标题",
        "content": "这是一篇测试文章的内容。AI技术正在快速发展，为内容创作带来新的可能性。",
        "word_count": 50,
        "outline": ["背景介绍", "技术现状", "未来展望"],
    })
    mock_service.generate_video_script = AsyncMock(return_value={
        "topic": "测试视频主题",
        "duration": 60,
        "script": "镜头1：开场介绍\n时长：5秒\n台词：欢迎观看",
        "shots": [
            {"description": "镜头1：开场介绍", "duration": "5秒", "dialogue": "欢迎观看"},
            {"description": "镜头2：内容展示", "duration": "10秒", "dialogue": "今天介绍的是..."},
        ],
    })
    mock_service.generate_text = AsyncMock(return_value="模拟生成的文本内容")
    return mock_service


@pytest.fixture
def mock_image_service():
    mock_service = MagicMock()
    mock_service.generate_image = AsyncMock(return_value={
        "url": "https://example.com/image.png",
        "revised_prompt": "A professional image",
    })
    mock_service.generate_cover_image = AsyncMock(return_value="https://example.com/cover.png")
    mock_service.generate_video_thumbnail = AsyncMock(return_value="https://example.com/thumbnail.png")
    return mock_service


class TestCreationAgent:
    @pytest.mark.asyncio
    async def test_creation_agent_initialization(self, creation_agent):
        assert creation_agent.name == "CreationAgent"
        assert creation_agent.llm_service is not None
        assert creation_agent.image_service is not None

    @pytest.mark.asyncio
    async def test_creation_agent_has_execute_method(self, creation_agent):
        assert hasattr(creation_agent, "execute")
        assert callable(creation_agent.execute)

    @pytest.mark.asyncio
    async def test_creation_agent_has_create_article_method(self, creation_agent):
        assert hasattr(creation_agent, "create_article")
        assert callable(creation_agent.create_article)

    @pytest.mark.asyncio
    async def test_creation_agent_has_create_video_content_method(self, creation_agent):
        assert hasattr(creation_agent, "create_video_content")
        assert callable(creation_agent.create_video_content)

    @pytest.mark.asyncio
    async def test_creation_agent_has_create_image_text_method(self, creation_agent):
        assert hasattr(creation_agent, "create_image_text")
        assert callable(creation_agent.create_image_text)


class TestCreationAgentArticle:
    @pytest.mark.asyncio
    async def test_create_article_success(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_article_001",
            params={
                "content_type": "article",
                "topic": "AI技术发展趋势",
                "outline": ["背景介绍", "技术现状", "未来展望"],
                "style": "professional",
                "generate_cover": True,
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        assert "title" in output.data
        assert "content" in output.data
        assert "cover_image_url" in output.data
        assert output.data["title"] == "AI技术发展趋势"

    @pytest.mark.asyncio
    async def test_create_article_without_cover(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_article_002",
            params={
                "content_type": "article",
                "topic": "AI技术发展趋势",
                "outline": ["背景介绍", "技术现状", "未来展望"],
                "style": "professional",
                "generate_cover": False,
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        assert "title" in output.data
        assert "content" in output.data
        assert "cover_image_url" not in output.data

    @pytest.mark.asyncio
    async def test_create_article_with_empty_outline(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_article_003",
            params={
                "content_type": "article",
                "topic": "测试主题",
                "outline": [],
                "style": "professional",
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        assert "title" in output.data

    @pytest.mark.asyncio
    async def test_create_article_direct_call(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_article_004",
            params={
                "topic": "直接调用测试",
                "outline": ["章节1", "章节2"],
                "style": "casual",
            }
        )

        result = await creation_agent.create_article(input_data)

        assert "title" in result
        assert "content" in result


class TestCreationAgentVideo:
    @pytest.mark.asyncio
    async def test_create_video_content_success(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_video_001",
            params={
                "content_type": "video",
                "topic": "产品介绍",
                "duration": 60,
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        assert "topic" in output.data
        assert "duration" in output.data
        assert "script" in output.data
        assert "shots" in output.data
        assert "frames" in output.data
        assert output.data["topic"] == "产品介绍"
        assert output.data["duration"] == 60

    @pytest.mark.asyncio
    async def test_create_video_content_with_custom_duration(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_video_002",
            params={
                "content_type": "video",
                "topic": "短视频教程",
                "duration": 30,
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        assert output.data["duration"] == 30

    @pytest.mark.asyncio
    async def test_create_video_content_default_duration(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_video_003",
            params={
                "content_type": "video",
                "topic": "无时长指定视频",
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        assert output.data["duration"] == 60

    @pytest.mark.asyncio
    async def test_create_video_content_generates_frames(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_video_004",
            params={
                "content_type": "video",
                "topic": "分帧测试",
                "duration": 60,
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        frames = output.data.get("frames", [])
        assert len(frames) > 0
        for frame in frames:
            assert "shot_number" in frame
            assert "description" in frame
            assert "dialogue" in frame
            assert "duration" in frame
            assert "image_url" in frame


class TestCreationAgentImageText:
    @pytest.mark.asyncio
    async def test_create_image_text_success(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_imagetext_001",
            params={
                "content_type": "image_text",
                "topic": "端午节活动",
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        assert "topic" in output.data
        assert "image_url" in output.data
        assert "infographic_prompt" in output.data
        assert output.data["topic"] == "端午节活动"

    @pytest.mark.asyncio
    async def test_create_image_text_direct_call(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_imagetext_002",
            params={
                "topic": "直接调用图文",
            }
        )

        result = await creation_agent.create_image_text(input_data)

        assert "topic" in result
        assert "image_url" in result


class TestCreationAgentEdgeCases:
    @pytest.mark.asyncio
    async def test_unsupported_content_type_raises_error(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_unsupported_001",
            params={
                "content_type": "unsupported_type",
                "topic": "测试",
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is False
        assert output.error is not None
        assert "Unsupported content type" in output.error

    @pytest.mark.asyncio
    async def test_execution_time_is_recorded(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_time_001",
            params={
                "content_type": "article",
                "topic": "测试",
                "outline": ["章节"],
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        assert output.execution_time >= 0
        assert isinstance(output.execution_time, float)

    @pytest.mark.asyncio
    async def test_timestamp_is_recorded(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        before_test = datetime.now()

        input_data = AgentInput(
            task_id="test_timestamp_001",
            params={
                "content_type": "article",
                "topic": "测试",
                "outline": ["章节"],
            }
        )

        output = await creation_agent.execute(input_data)

        after_test = datetime.now()

        assert output.timestamp >= before_test
        assert output.timestamp <= after_test

    @pytest.mark.asyncio
    async def test_article_with_empty_topic(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_empty_topic_001",
            params={
                "content_type": "article",
                "topic": "",
                "outline": ["章节"],
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        assert "title" in output.data

    @pytest.mark.asyncio
    async def test_video_with_empty_topic(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_empty_topic_002",
            params={
                "content_type": "video",
                "topic": "",
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        assert "script" in output.data


class TestCreationAgentWithMockLLMService:
    @pytest.mark.asyncio
    async def test_llm_service_generate_article_called(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_llm_call_001",
            params={
                "content_type": "article",
                "topic": "测试文章",
                "outline": ["章节1", "章节2"],
                "style": "professional",
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        mock_llm_service.generate_article.assert_called_once()
        call_args = mock_llm_service.generate_article.call_args
        assert call_args[0][0] == "测试文章"
        assert call_args[0][1] == ["章节1", "章节2"]
        assert call_args[0][2] == "professional"

    @pytest.mark.asyncio
    async def test_llm_service_generate_video_script_called(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_llm_call_002",
            params={
                "content_type": "video",
                "topic": "测试视频",
                "duration": 45,
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        mock_llm_service.generate_video_script.assert_called_once()
        call_args = mock_llm_service.generate_video_script.call_args
        assert call_args[0][0] == "测试视频"
        assert call_args[0][1] == 45

    @pytest.mark.asyncio
    async def test_image_service_generate_cover_image_called(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_image_call_001",
            params={
                "content_type": "article",
                "topic": "测试文章",
                "outline": ["章节"],
                "generate_cover": True,
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        mock_image_service.generate_cover_image.assert_called_once()
        assert mock_image_service.generate_cover_image.call_args[0][0] == "测试文章"


class TestCreationAgentOutputStructure:
    @pytest.mark.asyncio
    async def test_article_output_structure(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_structure_001",
            params={
                "content_type": "article",
                "topic": "测试",
                "outline": ["章节"],
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        data = output.data
        
        assert "title" in data
        assert "content" in data
        assert data["title"] == "测试文章标题"
        assert isinstance(data["content"], str)
        assert "word_count" in data
        assert "outline" in data

    @pytest.mark.asyncio
    async def test_video_output_structure(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_structure_002",
            params={
                "content_type": "video",
                "topic": "测试",
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        data = output.data
        
        assert "topic" in data
        assert "duration" in data
        assert "script" in data
        assert "shots" in data
        assert "frames" in data
        assert isinstance(data["shots"], list)

    @pytest.mark.asyncio
    async def test_image_text_output_structure(self, creation_agent, mock_llm_service, mock_image_service):
        creation_agent.llm_service = mock_llm_service
        creation_agent.image_service = mock_image_service

        input_data = AgentInput(
            task_id="test_structure_003",
            params={
                "content_type": "image_text",
                "topic": "测试",
            }
        )

        output = await creation_agent.execute(input_data)

        assert output.success is True
        data = output.data
        
        assert "topic" in data
        assert "image_url" in data
        assert "infographic_prompt" in data
