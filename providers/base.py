from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ToolCall:
    name: str
    args: dict
    id: str | None = None


@dataclass
class LLMResponse:
    text: str | None
    tool_calls: list[ToolCall] = field(default_factory=list)
    raw_model_content: object = None  # provider-native message to append to history
    prompt_tokens: int = 0
    response_tokens: int = 0


class LLMProvider(ABC):
    """Interface any LLM backend must implement so agent.py never
    touches a vendor-specific SDK directly."""

    @abstractmethod
    def generate(self, messages: list, system_prompt: str) -> LLMResponse | None:
        """Send the conversation so far and get back text or tool calls.
        Returns None on a handled error (e.g. quota exceeded)."""
        ...

    @abstractmethod
    def format_tool_result(self, tool_call: ToolCall, result: object) -> object:
        """Convert a tool's result into this provider's expected message format."""
        ...