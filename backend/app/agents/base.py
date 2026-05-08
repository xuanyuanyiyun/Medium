from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AgentInput(BaseModel):
    task_id: str
    params: Dict[str, Any] = {}
    context: Dict[str, Any] = {}


class AgentOutput(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = datetime.now()


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")

    @abstractmethod
    async def execute(self, input_data: AgentInput) -> AgentOutput:
        pass

    async def validate_input(self, input_data: AgentInput) -> bool:
        return True

    def log_start(self, input_data: AgentInput):
        self.logger.info(f"[{self.name}] Task {input_data.task_id} started")

    def log_complete(self, input_data: AgentInput, output: AgentOutput):
        if output.success:
            self.logger.info(
                f"[{self.name}] Task {input_data.task_id} completed "
                f"in {output.execution_time:.2f}s"
            )
        else:
            self.logger.error(
                f"[{self.name}] Task {input_data.task_id} failed: {output.error}"
            )
