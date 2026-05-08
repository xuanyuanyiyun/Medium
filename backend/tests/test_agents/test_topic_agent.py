import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from app.agents.topic_agent import TopicAgent
from app.agents.base import AgentInput, AgentOutput


@pytest.fixture
def topic_agent():
    return TopicAgent()


@pytest.fixture
def mock_hot_topic_service(mock_hot_topic_data):
    mock_service = MagicMock()
    mock_service.fetch_all = AsyncMock(return_value=mock_hot_topic_data)
    mock_service.fetch_weibo_hot = AsyncMock(return_value=mock_hot_topic_data[:2])
    mock_service.fetch_zhihu_hot = AsyncMock(return_value=mock_hot_topic_data[2:3])
    mock_service.fetch_douyin_trending = AsyncMock(return_value=mock_hot_topic_data[3:4])
    mock_service.fetch_xiaohongshu_trending = AsyncMock(return_value=mock_hot_topic_data[4:])
    return mock_service


class TestTopicAgent:
    @pytest.mark.asyncio
    async def test_topic_agent_initialization(self, topic_agent):
        assert topic_agent.name == "TopicAgent"
        assert topic_agent.hot_topic_service is not None

    @pytest.mark.asyncio
    async def test_topic_agent_has_execute_method(self, topic_agent):
        assert hasattr(topic_agent, "execute")
        assert callable(topic_agent.execute)

    @pytest.mark.asyncio
    async def test_topic_agent_has_fetch_hot_topics_method(self, topic_agent):
        assert hasattr(topic_agent, "fetch_hot_topics")
        assert callable(topic_agent.fetch_hot_topics)

    @pytest.mark.asyncio
    async def test_topic_agent_has_generate_topic_suggestions_method(self, topic_agent):
        assert hasattr(topic_agent, "generate_topic_suggestions")
        assert callable(topic_agent.generate_topic_suggestions)

    @pytest.mark.asyncio
    async def test_topic_agent_has_analyze_topic_method(self, topic_agent):
        assert hasattr(topic_agent, "analyze_topic")
        assert callable(topic_agent.analyze_topic)


class TestTopicAgentFetchHotTopics:
    @pytest.mark.asyncio
    async def test_fetch_hot_topics_success(self, topic_agent, mock_hot_topic_service):
        topic_agent.hot_topic_service = mock_hot_topic_service
        
        input_data = AgentInput(
            task_id="test_fetch_001",
            params={"action": "fetch_hot_topics", "limit": 10}
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        assert "topics" in output.data
        assert isinstance(output.data["topics"], list)
        assert "total" in output.data
        assert "fetched_at" in output.data
        assert output.data["total"] == 5

    @pytest.mark.asyncio
    async def test_fetch_hot_topics_with_category_filter(self, topic_agent, mock_hot_topic_service):
        topic_agent.hot_topic_service = mock_hot_topic_service
        
        input_data = AgentInput(
            task_id="test_fetch_002",
            params={"action": "fetch_hot_topics", "category": "technology"}
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        topics = output.data["topics"]
        for topic in topics:
            assert topic["category"] == "technology"

    @pytest.mark.asyncio
    async def test_fetch_hot_topics_with_limit(self, topic_agent, mock_hot_topic_service):
        topic_agent.hot_topic_service = mock_hot_topic_service
        
        input_data = AgentInput(
            task_id="test_fetch_003",
            params={"action": "fetch_hot_topics", "limit": 2}
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        assert len(output.data["topics"]) == 2

    @pytest.mark.asyncio
    async def test_fetch_hot_topics_returns_sorted_by_heat_score(self, topic_agent, mock_hot_topic_service):
        topic_agent.hot_topic_service = mock_hot_topic_service
        
        input_data = AgentInput(
            task_id="test_fetch_004",
            params={"action": "fetch_hot_topics"}
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        topics = output.data["topics"]
        heat_scores = [t["heat_score"] for t in topics]
        assert heat_scores == sorted(heat_scores, reverse=True)

    @pytest.mark.asyncio
    async def test_fetch_hot_topics_with_region_filter_no_match(self, topic_agent, mock_hot_topic_service):
        topic_agent.hot_topic_service = mock_hot_topic_service
        
        input_data = AgentInput(
            task_id="test_fetch_005",
            params={"action": "fetch_hot_topics", "region": "beijing"}
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True


class TestTopicAgentGenerateSuggestions:
    @pytest.mark.asyncio
    async def test_generate_topic_suggestions_success(self, topic_agent):
        input_data = AgentInput(
            task_id="test_suggest_001",
            params={
                "action": "generate_topic_suggestions",
                "keyword": "人工智能"
            }
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        assert output.data["keyword"] == "人工智能"
        assert "suggestions" in output.data
        assert len(output.data["suggestions"]) == 3

    @pytest.mark.asyncio
    async def test_generate_topic_suggestions_structure(self, topic_agent):
        input_data = AgentInput(
            task_id="test_suggest_002",
            params={
                "action": "generate_topic_suggestions",
                "keyword": "短视频"
            }
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        suggestions = output.data["suggestions"]
        
        for suggestion in suggestions:
            assert "title" in suggestion
            assert "angle" in suggestion
            assert "outline" in suggestion
            assert isinstance(suggestion["outline"], list)

    @pytest.mark.asyncio
    async def test_generate_topic_suggestions_contains_keyword_in_titles(self, topic_agent):
        input_data = AgentInput(
            task_id="test_suggest_003",
            params={
                "action": "generate_topic_suggestions",
                "keyword": "AI"
            }
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        suggestions = output.data["suggestions"]
        
        for suggestion in suggestions:
            assert "AI" in suggestion["title"]

    @pytest.mark.asyncio
    async def test_generate_topic_suggestions_different_angles(self, topic_agent):
        input_data = AgentInput(
            task_id="test_suggest_004",
            params={
                "action": "generate_topic_suggestions",
                "keyword": "新媒体"
            }
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        suggestions = output.data["suggestions"]
        angles = [s["angle"] for s in suggestions]
        
        assert "深度分析" in angles
        assert "实用教程" in angles
        assert "行业视角" in angles


class TestTopicAgentAnalyzeTopic:
    @pytest.mark.asyncio
    async def test_analyze_topic_success(self, topic_agent):
        input_data = AgentInput(
            task_id="test_analyze_001",
            params={
                "action": "analyze_topic",
                "topic": "AI技术发展"
            }
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        assert output.data["topic"] == "AI技术发展"
        assert "heat_level" in output.data
        assert "competition_level" in output.data
        assert "audience" in output.data
        assert "best_publish_time" in output.data
        assert "related_keywords" in output.data

    @pytest.mark.asyncio
    async def test_analyze_topic_related_keywords_include_topic(self, topic_agent):
        input_data = AgentInput(
            task_id="test_analyze_002",
            params={
                "action": "analyze_topic",
                "topic": "内容创作"
            }
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        related_keywords = output.data["related_keywords"]
        
        for keyword in related_keywords:
            assert "内容创作" in keyword

    @pytest.mark.asyncio
    async def test_analyze_topic_with_empty_topic(self, topic_agent):
        input_data = AgentInput(
            task_id="test_analyze_003",
            params={
                "action": "analyze_topic",
                "topic": ""
            }
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        assert output.data["topic"] == ""


class TestTopicAgentEdgeCases:
    @pytest.mark.asyncio
    async def test_unknown_action_returns_error_data(self, topic_agent):
        input_data = AgentInput(
            task_id="test_unknown_001",
            params={"action": "unknown_action"}
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        assert "error" in output.data

    @pytest.mark.asyncio
    async def test_execute_uses_default_action(self, topic_agent, mock_hot_topic_service):
        topic_agent.hot_topic_service = mock_hot_topic_service
        
        input_data = AgentInput(
            task_id="test_default_001",
            params={}
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        assert "topics" in output.data

    @pytest.mark.asyncio
    async def test_execution_time_is_recorded(self, topic_agent, mock_hot_topic_service):
        topic_agent.hot_topic_service = mock_hot_topic_service
        
        input_data = AgentInput(
            task_id="test_time_001",
            params={"action": "fetch_hot_topics"}
        )
        
        output = await topic_agent.execute(input_data)
        
        assert output.success is True
        assert output.execution_time >= 0
        assert isinstance(output.execution_time, float)

    @pytest.mark.asyncio
    async def test_timestamp_is_recorded(self, topic_agent, mock_hot_topic_service):
        topic_agent.hot_topic_service = mock_hot_topic_service
        
        before_test = datetime.now()
        
        input_data = AgentInput(
            task_id="test_timestamp_001",
            params={"action": "fetch_hot_topics"}
        )
        
        output = await topic_agent.execute(input_data)
        
        after_test = datetime.now()
        
        assert output.timestamp >= before_test
        assert output.timestamp <= after_test


class TestTopicAgentDirectMethods:
    @pytest.mark.asyncio
    async def test_fetch_hot_topics_direct_call(self, topic_agent, mock_hot_topic_service):
        topic_agent.hot_topic_service = mock_hot_topic_service
        
        input_data = AgentInput(
            task_id="test_direct_001",
            params={"limit": 10}
        )
        
        result = await topic_agent.fetch_hot_topics(input_data)
        
        assert "topics" in result
        assert "total" in result
        assert "fetched_at" in result

    @pytest.mark.asyncio
    async def test_generate_topic_suggestions_direct_call(self, topic_agent):
        input_data = AgentInput(
            task_id="test_direct_002",
            params={"keyword": "测试"}
        )
        
        result = await topic_agent.generate_topic_suggestions(input_data)
        
        assert "keyword" in result
        assert "suggestions" in result

    @pytest.mark.asyncio
    async def test_analyze_topic_direct_call(self, topic_agent):
        input_data = AgentInput(
            task_id="test_direct_003",
            params={"topic": "测试主题"}
        )
        
        result = await topic_agent.analyze_topic(input_data)
        
        assert "topic" in result
        assert "heat_level" in result
        assert "competition_level" in result
