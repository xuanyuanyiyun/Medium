from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import time
from app.agents.base import BaseAgent, AgentInput, AgentOutput
from app.platforms.base import platform_manager


class AnalyticsAgent(BaseAgent):
    def __init__(self):
        super().__init__("AnalyticsAgent")

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        start_time = time.time()
        self.log_start(input_data)

        try:
            await self.validate_input(input_data)

            action = input_data.params.get("action", "fetch_analytics")
            
            if action == "fetch_analytics":
                result = await self.fetch_platform_analytics(input_data)
            elif action == "generate_report":
                result = await self.generate_analytics_report(input_data)
            elif action == "compare_periods":
                result = await self.compare_time_periods(input_data)
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

    async def fetch_platform_analytics(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        platform = input_data.params.get("platform")
        post_id = input_data.params.get("post_id")
        
        adapter = platform_manager.get_adapter(platform)
        
        if not adapter:
            raise ValueError(f"Platform not supported: {platform}")
        
        analytics = await adapter.get_analytics(post_id)
        
        return {
            "platform": platform,
            "post_id": post_id,
            "metrics": analytics,
            "fetched_at": datetime.now().isoformat(),
        }

    async def generate_analytics_report(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        distribution_ids = input_data.params.get("distribution_ids", [])
        
        metrics_summary = {
            "total_views": 0,
            "total_likes": 0,
            "total_comments": 0,
            "total_shares": 0,
            "total_saves": 0,
            "engagement_rate": 0.0,
            "avg_completion_rate": 0.0,
        }
        
        for dist_id in distribution_ids:
            metrics_summary["total_views"] += 1000
            metrics_summary["total_likes"] += 100
            metrics_summary["total_comments"] += 20
            metrics_summary["total_shares"] += 10
            metrics_summary["total_saves"] += 15
        
        if metrics_summary["total_views"] > 0:
            metrics_summary["engagement_rate"] = round(
                (metrics_summary["total_likes"] + metrics_summary["total_comments"] +
                 metrics_summary["total_shares"] + metrics_summary["total_saves"]) /
                metrics_summary["total_views"] * 100,
                2
            )
        
        chart_data = [
            {
                "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                "views": 1000 - i * 50,
                "likes": 100 - i * 5,
                "comments": 20 - i,
            }
            for i in range(7)
        ][::-1]
        
        platform_breakdown = [
            {"platform": "wechat", "views": 5000, "engagement_rate": 8.5},
            {"platform": "weibo", "views": 3500, "engagement_rate": 6.2},
            {"platform": "douyin", "views": 8000, "engagement_rate": 12.3},
        ]
        
        top_content = [
            {"title": "爆款文章", "views": 5000, "engagement": "8.5%", "platform": "wechat"},
            {"title": "热点视频", "views": 3500, "engagement": "12.3%", "platform": "douyin"},
            {"title": "深度分析", "views": 2800, "engagement": "7.8%", "platform": "weibo"},
        ]
        
        content_type_breakdown = [
            {"type": "article", "count": 15, "avg_views": 2500, "avg_engagement": 6.5},
            {"type": "video", "count": 8, "avg_views": 5000, "avg_engagement": 10.2},
            {"type": "image_text", "count": 12, "avg_views": 1800, "avg_engagement": 5.8},
        ]
        
        return {
            "summary": metrics_summary,
            "chart_data": chart_data,
            "platform_breakdown": platform_breakdown,
            "top_content": top_content,
            "content_type_breakdown": content_type_breakdown,
            "period": "最近7天",
            "generated_at": datetime.now().isoformat(),
        }

    async def compare_time_periods(
        self,
        input_data: AgentInput,
    ) -> Dict[str, Any]:
        current_metrics = input_data.params.get("current_metrics", {})
        previous_metrics = input_data.params.get("previous_metrics", {})
        
        def calculate_change(current: int, previous: int) -> Dict[str, Any]:
            change_percent = 0
            if previous > 0:
                change_percent = round(((current - previous) / previous) * 100, 2)
            
            return {
                "current": current,
                "previous": previous,
                "change_percent": change_percent,
                "absolute_change": current - previous,
                "trend": "up" if change_percent > 0 else "down" if change_percent < 0 else "stable",
            }
        
        comparison = {
            "views": calculate_change(
                current_metrics.get("views", 0),
                previous_metrics.get("views", 0)
            ),
            "likes": calculate_change(
                current_metrics.get("likes", 0),
                previous_metrics.get("likes", 0)
            ),
            "comments": calculate_change(
                current_metrics.get("comments", 0),
                previous_metrics.get("comments", 0)
            ),
            "shares": calculate_change(
                current_metrics.get("shares", 0),
                previous_metrics.get("shares", 0)
            ),
            "engagement_rate": calculate_change(
                current_metrics.get("engagement_rate", 0),
                previous_metrics.get("engagement_rate", 0)
            ),
        }
        
        overall_change = 0
        previous_total = sum(previous_metrics.values())
        current_total = sum(current_metrics.values())
        if previous_total > 0:
            overall_change = round(((current_total - previous_total) / previous_total) * 100, 2)
        
        return {
            "period_comparison": {
                "current_period": input_data.params.get("current_period", "最近7天"),
                "previous_period": input_data.params.get("previous_period", "上一个7天"),
            },
            "metrics_comparison": comparison,
            "overall_trend": {
                "change_percent": overall_change,
                "trend": "up" if overall_change > 0 else "down" if overall_change < 0 else "stable",
            },
            "insights": self._generate_insights(comparison),
            "generated_at": datetime.now().isoformat(),
        }

    def _generate_insights(self, comparison: Dict[str, Any]) -> List[str]:
        insights = []
        
        for metric, data in comparison.items():
            if data["trend"] == "up" and data["change_percent"] > 10:
                insights.append(f"{metric}表现优秀，较上期增长{data['change_percent']}%")
            elif data["trend"] == "down" and data["change_percent"] < -10:
                insights.append(f"{metric}有所下降，建议关注内容质量")
        
        if not insights:
            insights.append("各项指标表现稳定，继续保持当前策略")
        
        return insights

    async def get_platform_summary(
        self,
        platforms: List[str],
    ) -> Dict[str, Any]:
        platform_summaries = []
        
        for platform_name in platforms:
            adapter = platform_manager.get_adapter(platform_name)
            
            if adapter:
                platform_summaries.append({
                    "platform": platform_name,
                    "status": "connected",
                    "supported_features": ["publish", "analytics", "status_check"],
                })
            else:
                platform_summaries.append({
                    "platform": platform_name,
                    "status": "not_configured",
                    "supported_features": [],
                })
        
        return {
            "platforms": platform_summaries,
            "total_platforms": len(platforms),
            "connected_count": sum(1 for p in platform_summaries if p["status"] == "connected"),
            "fetched_at": datetime.now().isoformat(),
        }
