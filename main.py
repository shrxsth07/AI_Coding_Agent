import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from Functions.get_files_info import schema_get_files_info
from Functions.get_file_content import schema_get_file_content
from Functions.write_file import schema_write_file
from Functions.run_python_file import schema_run_python_file

from call_function import call_function


def main():
    load_dotenv()  # Load the variables stored in the .env file

    # Get the Gemini API key from the environment
    api_key = os.environ.get("GEMINI_API_KEY")

    # Create a Gemini client using our API key
    client = genai.Client(api_key=api_key)

    # General guide for the AI Agent
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan.
        You can perform the following operations:

        - List files and directories
        - Read the contents of a file
        - Write or overwrite files
        - Run Python files

        All paths you provide should be relative to the working directory.
        The working directory is "calculator".

        Do not include "calculator/" in file paths.
        For example, use "main.py" instead of "calculator/main.py".

        You do not need to specify the working directory in your function calls
        as it is automatically injected for security reasons.
    """

    if len(sys.argv) < 2:
        print("I need a prompt!")
        sys.exit(1)

    # sys.argv[0] = name of the Python file
    # sys.argv[1] = user's prompt
    prompt = sys.argv[1]

    verbose_flag = False

    # Check if --verbose was provided
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    # Create a message that Gemini can understand
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        ),
    ]

    # Give Gemini access to all our available tools
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    # Send the user's request to Gemini
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )

    # Make sure usage information exists before accessing it
    if response is None or response.usage_metadata is None:
        print("Response is malformed")
        return

    # Print token information only in verbose mode
    if verbose_flag:
        print(f"User prompt: {prompt}")

        print(
            f"Prompt tokens: "
            f"{response.usage_metadata.prompt_token_count}"
        )

        print(
            f"Response tokens: "
            f"{response.usage_metadata.candidates_token_count}"
        )

    # Check if Gemini wants to call a function
    if response.function_calls:
        for function_call_part in response.function_calls:

            # Actually execute the function Gemini requested
            function_call_result = call_function(
                function_call_part,
                "calculator",
                verbose_flag
            )

            # Print the result returned by our function
            print(function_call_result)

    else:
        # If Gemini didn't request a function, print its normal response
        print(response.text)


if __name__ == "__main__":
    main()