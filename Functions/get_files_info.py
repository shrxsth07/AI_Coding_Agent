import os
from google.genai import types
from Functions.safety import resolve_safe_path, PathTraversalError


def get_files_info(working_directory, directory="."):
    try:
        abs_directory = resolve_safe_path(working_directory, directory)
    except PathTraversalError as e:
        return f"Error: {e}"

    if not os.path.isdir(abs_directory):
        return f"Error: '{directory}' is not a directory"

    try:
        contents = os.listdir(abs_directory)
    except Exception as e:
        return f"Error listing directory: {e}"

    final_response = ""
    for content in contents:
        content_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        final_response += f"- {content}: file_size={size} bytes, is_dir={is_dir}\n"

    return final_response


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "Lists files in a specified directory relative to the "
        "working directory, providing file size and directory status."
    ),
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "directory": types.Schema(
                type="STRING",
                description=(
                    "Directory path to list files from, relative to "
                    "the working directory. Default is the working "
                    "directory itself."
                ),
            ),
        },
    ),
)