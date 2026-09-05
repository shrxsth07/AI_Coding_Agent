import os
from google.genai import types
from config import MAX_CHARS
from Functions.safety import resolve_safe_path, PathTraversalError


def get_file_content(working_directory, file_path):
    try:
        abs_file_path = resolve_safe_path(working_directory, file_path)
    except PathTraversalError as e:
        return f"Error: {e}"

    if not os.path.isfile(abs_file_path):
        return f"Error: '{file_path}' is not a file"

    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += (
                    f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content_string
    except Exception as e:
        return f"Exception reading file: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Reads the contents of a file within the working directory. "
        "The file path must be relative to the working directory."
    ),
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "file_path": types.Schema(
                type="STRING",
                description=(
                    "Path to the file to read, relative to the "
                    "working directory."
                ),
            ),
        },
        required=["file_path"],
    ),
)