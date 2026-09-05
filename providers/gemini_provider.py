from google import genai
from google.genai import types

from providers.base import LLMProvider, LLMResponse, ToolCall
from Functions.get_files_info import schema_get_files_info
from Functions.get_file_content import schema_get_file_content
from Functions.write_file import schema_write_file
from Functions.run_python_file import schema_run_python_file


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-3.6-flash", verbose: bool = False):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.verbose = verbose
        self.tools = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_write_file,
                schema_run_python_file,
            ]
        )

    def generate(self, messages, system_prompt) -> LLMResponse | None:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[self.tools],
                ),
            )
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                print("Error: Gemini API quota limit reached.")
                print("Please try again later.")
            else:
                print(f"Error communicating with Gemini: {e}")
            return None

        if not response.candidates:
            print("No candidates returned.")
            return None

        if self.verbose and response.usage_metadata:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        tool_calls = [
            ToolCall(name=fc.name, args=fc.args, id=fc.id)
            for fc in (response.function_calls or [])
        ]

        return LLMResponse(
            text=response.text,
            tool_calls=tool_calls,
            raw_model_content=response.candidates[0].content,
        )

    def format_tool_result(self, tool_call: ToolCall, result) -> types.Content:
        return types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=tool_call.name,
                    response={"result": result},
                    id=tool_call.id,
                )
            ],
        )