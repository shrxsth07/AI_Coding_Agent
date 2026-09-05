import os
from google import genai
from google.genai import types

from Functions.get_files_info import schema_get_files_info
from Functions.get_file_content import schema_get_file_content
from Functions.write_file import schema_write_file
from Functions.run_python_file import schema_run_python_file
from call_function import call_function

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
    def __init__(self, api_key: str, working_directory: str, max_iters: int = 5, verbose: bool = False):
        self.client = genai.Client(api_key=api_key)
        self.working_directory = working_directory
        self.max_iters = max_iters
        self.verbose = verbose
        self.available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_write_file,
                schema_run_python_file,
            ]
        )

    def run(self, prompt: str) -> str:
        """Runs the agent loop for a single prompt and returns the final text response."""
        messages = [
            types.Content(
                role="user",
                parts=[types.Part(text=prompt)],
            )
        ]

        for _ in range(self.max_iters):
            response = self._generate(messages, prompt)
            if response is None:
                return "Error: no response from model."

            if not response.candidates:
                return "Error: no candidates returned."

            model_content = response.candidates[0].content
            if model_content is not None:
                messages.append(model_content)

            if response.function_calls:
                for function_call_part in response.function_calls:
                    function_call_result = call_function(
                        function_call_part,
                        self.working_directory,
                        self.verbose,
                    )
                    messages.append(function_call_result)
                continue

            return response.text

        return "Maximum iterations reached."

    def _generate(self, messages, prompt):
        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=[self.available_functions],
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

        if self.verbose and response.usage_metadata:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        return response