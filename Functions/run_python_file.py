import os
import subprocess
import sys
from google.genai import types
from Functions.safety import resolve_safe_path, PathTraversalError


def run_python_file(working_directory: str, file_path: str, args=None):
    if args is None:
        args = []

    try:
        abs_file_path = resolve_safe_path(working_directory, file_path)
    except PathTraversalError as e:
        return f"Error: {e}"

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        final_args = [sys.executable, file_path] + args
        output = subprocess.run(
            final_args,
            cwd=os.path.abspath(working_directory),
            timeout=30,
            capture_output=True,
            text=True,
        )
        final_string = f"STDOUT: {output.stdout}\nSTDERR: {output.stderr}\n"
        if output.stdout == "" and output.stderr == "":
            final_string = "No output produced.\n"
        if output.returncode != 0:
            final_string += f"Process exited with code {output.returncode}"
        return final_string
    except subprocess.TimeoutExpired:
        return f'Error: execution of "{file_path}" timed out after 30 seconds'
    except Exception as e:
        return f"Error executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file within the working directory and "
        "returns its output. The file must be a Python (.py) file."
    ),
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "file_path": types.Schema(
                type="STRING",
                description=(
                    "Path to the Python file to execute, relative to "
                    "the working directory."
                ),
            ),
            "args": types.Schema(
                type="ARRAY",
                items=types.Schema(type="STRING"),
                description=(
                    "Optional command-line arguments to pass to the "
                    "Python file."
                ),
            ),
        },
        required=["file_path"],
    ),
)