from typing import Optional, List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
import os


class LLMService:
    def __init__(self):
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        
        self.openai_llm = ChatOpenAI(
            model=self.openai_model,
            temperature=0.7,
        )
        
        self.anthropic_llm = ChatAnthropic(
            model=self.anthropic_model,
            temperature=0.7,
        )

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        provider: str = "openai",
        **kwargs
    ) -> str:
        messages = []
        
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        messages.append(HumanMessage(content=prompt))
        
        if provider == "anthropic":
            response = await self.anthropic_llm.agenerate([messages])
        else:
            response = await self.openai_llm.agenerate([messages])
        
        return response.generations[0][0].text

    async def generate_article(
        self,
        topic: str,
        outline: List[str],
        style: str = "professional",
    ) -> Dict[str, Any]:
        system_prompt = f"""你是一位专业的{style}风格内容创作者，擅长撰写吸引读者的文章。
要求：
1. 文章结构清晰，内容充实
2. 语言流畅，逻辑严密
3. 适当使用小标题和列表增强可读性
4. 避免敏感内容和虚假信息"""

        prompt = f"""请根据以下主题和大纲撰写文章：

主题：{topic}

大纲：
{chr(10).join([f"{i+1}. {item}" for i, item in enumerate(outline)])}

请按照大纲结构撰写完整的文章内容。"""

        content = await self.generate_text(prompt, system_prompt)
        
        return {
            "title": topic,
            "content": content,
            "word_count": len(content),
            "outline": outline,
        }

    async def generate_video_script(
        self,
        topic: str,
        duration: int = 60,
    ) -> Dict[str, Any]:
        system_prompt = """你是一位专业的视频编导，擅长创作吸引人的短视频脚本。
要求：
1. 开场3秒要抓住观众注意力
2. 每个镜头时长控制在5-15秒
3. 包含明确的画面描述和台词
4. 节奏紧凑，避免冗长"""

        prompt = f"""请为以下主题创作一个{duration}秒的短视频分镜脚本：

主题：{topic}

请输出包含以下字段的分镜脚本：
- 镜头序号
- 画面描述
- 台词/解说
- 时长
- 音效/配乐建议"""

        script = await self.generate_text(prompt, system_prompt)
        
        return {
            "topic": topic,
            "duration": duration,
            "script": script,
            "shots": self._parse_shots(script),
        }

    def _parse_shots(self, script: str) -> List[Dict[str, Any]]:
        shots = []
        lines = script.split("\n")
        current_shot = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith("镜头") or line.startswith("Shot"):
                if current_shot:
                    shots.append(current_shot)
                current_shot = {"description": line}
            elif line.startswith("时长"):
                current_shot["duration"] = line.split("：")[-1]
            elif line.startswith("台词") or line.startswith("解说"):
                current_shot["dialogue"] = line.split("：")[-1]
        
        if current_shot:
            shots.append(current_shot)
        
        return shots


llm_service = LLMService()
