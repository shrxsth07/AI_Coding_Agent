from agent import CodingAgent
from providers.fake_provider import FakeProvider
from providers.base import LLMResponse, ToolCall

# Script the fake model's behavior turn by turn:
# Turn 1: model asks to list files
# Turn 2: model says it's done
scripted = [
    LLMResponse(
        text=None,
        tool_calls=[ToolCall(name="get_files_info", args={}, id="call_1")],
        raw_model_content=None,
    ),
    LLMResponse(
        text="I found the files. Done!",
        tool_calls=[],
        raw_model_content=None,
    ),
]

provider = FakeProvider(scripted)
agent = CodingAgent(provider=provider, working_directory="test_fixtures/calculator", verbose=True)

result = agent.run("list the files here")
print("----")
print("FINAL RESULT:", result)