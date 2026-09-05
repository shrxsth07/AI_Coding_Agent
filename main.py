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
    load_dotenv()

    # The directory from which the agent is being executed.
    # All file operations are restricted to this directory.
    working_directory = os.getcwd()

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY is not set.")
        return

    client = genai.Client(api_key=api_key)

    system_prompt = """
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

    if len(sys.argv) < 2:
        print("I need a prompt!")
        sys.exit(1)

    prompt = sys.argv[1]

    verbose_flag = False

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    # Initial user message
    messages = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=prompt)
            ],
        )
    ]

    # All tools available to Gemini
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    max_iters = 5

    for _ in range(max_iters):

        # Ask Gemini what to do next
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions],
                ),
            )

        except Exception as e:
            error_message = str(e)

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                print("Error: Gemini API quota limit reached.")
                print("Please try again later.")
            else:
                print(f"Error communicating with Gemini: {e}")

            return

        if response is None:
            print("Response is malformed.")
            return

        # Verbose token information
        if verbose_flag and response.usage_metadata:
            print(f"User prompt: {prompt}")

            print(
                f"Prompt tokens: "
                f"{response.usage_metadata.prompt_token_count}"
            )

            print(
                f"Response tokens: "
                f"{response.usage_metadata.candidates_token_count}"
            )

        # Make sure Gemini returned a candidate
        if not response.candidates:
            print("No candidates returned.")
            return

        # Add Gemini's complete response to the conversation.
        #
        # This is important because it preserves the function call
        # and its thought_signature.
        model_content = response.candidates[0].content

        if model_content is not None:
            messages.append(model_content)

        # Gemini wants to call one or more functions
        if response.function_calls:

            for function_call_part in response.function_calls:

                function_call_result = call_function(
                    function_call_part,
                    working_directory,
                    verbose_flag,
                )

                # Add the function result to the conversation
                messages.append(function_call_result)

            # Gemini will receive the function result
            # on the next iteration.
            continue

        # Gemini has finished
        print(response.text)
        return

    print("Maximum iterations reached.")


if __name__ == "__main__":
    main()