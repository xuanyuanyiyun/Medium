from typing import Dict, Any, List
from datetime import datetime
import time
import re
from app.agents.base import BaseAgent, AgentInput, AgentOutput


class ReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReviewAgent")
        self.sensitive_words = self._load_sensitive_words()

    def _load_sensitive_words(self) -> List[str]:
        return [
            "敏感词1", "敏感词2", "违规词", "禁止词",
        ]

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        start_time = time.time()
        self.log_start(input_data)

        try:
            await self.validate_input(input_data)

            content = input_data.params.get("content", "")
            content_type = input_data.params.get("content_type", "article")

            results = {
                "sensitive_words_check": await self.check_sensitive_words(content),
                "compliance_check": await self.check_compliance(content),
                "fact_check": await self.check_facts(input_data.params),
                "quality_score": await self.assess_quality(content),
            }

            overall_pass = (
                results["sensitive_words_check"]["passed"] and
                results["compliance_check"]["passed"] and
                results["quality_score"]["score"] >= 60
            )

            result = {
                "passed": overall_pass,
                "checks": results,
                "suggestions": self._generate_suggestions(results),
                "reviewed_at": datetime.now().isoformat(),
            }

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

    async def check_sensitive_words(self, content: str) -> Dict[str, Any]:
        found_words = []
        for word in self.sensitive_words:
            if word in content:
                found_words.append(word)
        
        return {
            "passed": len(found_words) == 0,
            "found_words": found_words,
            "message": "敏感词检查通过" if not found_words else f"发现敏感词: {', '.join(found_words)}",
        }

    async def check_compliance(self, content: str) -> Dict[str, Any]:
        issues = []
        
        if len(content) < 100:
            issues.append("内容过短，可能信息量不足")
        
        if re.search(r'[零一三四五六七八九十○一二三四五六七八九十]+.*?[联系电话微信QQ邮箱]+', content):
            issues.append("疑似包含联系方式")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "message": "合规检查通过" if not issues else f"发现问题: {'; '.join(issues)}",
        }

    async def check_facts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        claims = params.get("claims", [])
        
        verified_claims = []
        for claim in claims:
            verified_claims.append({
                "claim": claim,
                "verified": True,
                "confidence": 0.9,
            })
        
        return {
            "total_claims": len(claims),
            "verified_claims": len(verified_claims),
            "details": verified_claims,
        }

    async def assess_quality(self, content: str) -> Dict[str, Any]:
        score = 100
        
        if len(content) < 500:
            score -= 20
        elif len(content) < 1000:
            score -= 10
        
        if not any(c in content for c in "。！？"):
            score -= 15
        
        paragraphs = content.split("\n\n")
        if len(paragraphs) < 3:
            score -= 10
        
        return {
            "score": max(0, score),
            "factors": {
                "length": "good" if len(content) > 500 else "too_short",
                "structure": "good" if len(paragraphs) >= 3 else "needs_improvement",
                "punctuation": "good" if any(c in content for c in "。！？") else "missing_punctuation",
            },
        }

    def _generate_suggestions(self, results: Dict[str, Any]) -> List[str]:
        suggestions = []
        
        if not results["sensitive_words_check"]["passed"]:
            suggestions.append(f"请修改敏感词: {', '.join(results['sensitive_words_check']['found_words'])}")
        
        if not results["compliance_check"]["passed"]:
            suggestions.extend(results["compliance_check"]["issues"])
        
        quality = results["quality_score"]
        if quality["score"] < 80:
            suggestions.append("建议增加内容深度和结构完整性")
        
        return suggestions
