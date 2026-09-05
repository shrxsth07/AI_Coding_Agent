from google.genai import types
from call_function import call_function
from providers.base import LLMProvider

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.
You can perform the following operations:

- List files and directories
- Read the contents of a file
- Write or overwrite files
- Run Python files

All paths you provide should be relative to the working directory.
Do not use absolute paths.
Do not attempt to access files outside the working directory.
The working directory is automatically provided by the application.
"""


class CodingAgent:
    def __init__(self, provider: LLMProvider, working_directory: str, max_iters: int = 5, verbose: bool = False):
        self.provider = provider
        self.working_directory = working_directory
        self.max_iters = max_iters
        self.verbose = verbose

    def run(self, prompt: str) -> str:
        messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

        for _ in range(self.max_iters):
            response = self.provider.generate(messages, SYSTEM_PROMPT)
            if response is None:
                return "Error: no response from model."

            if response.raw_model_content is not None:
                messages.append(response.raw_model_content)

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    result = call_function(
                        tool_call,
                        self.working_directory,
                        self.verbose,
                    )
                    formatted = self.provider.format_tool_result(tool_call, result)
                    messages.append(formatted)
                continue

            return response.text

        return "Maximum iterations reached."