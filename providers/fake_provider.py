from providers.base import LLMProvider, LLMResponse, ToolCall


class FakeProvider(LLMProvider):
    """A stand-in provider for testing the agent loop without calling any real API.
    You control what it 'says' by passing a script of responses in order."""

    def __init__(self, scripted_responses: list[LLMResponse]):
        self._responses = list(scripted_responses)
        self._call_count = 0

    def generate(self, messages, system_prompt):
        if self._call_count >= len(self._responses):
            raise RuntimeError("FakeProvider ran out of scripted responses")
        response = self._responses[self._call_count]
        self._call_count += 1
        return response

    def format_tool_result(self, tool_call, result):
        # Just a plain dict is fine for testing — no real message shaping needed.
        return {"role": "tool_result", "name": tool_call.name, "result": result}