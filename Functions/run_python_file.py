import os
import subprocess
import sys

from google.genai import types

def run_python_file(working_directory: str, file_path: str, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working dir'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        final_args=[sys.executable, file_path]
        final_args.extend(args)
        output = subprocess.run(
            final_args,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True,
        )
        final_string = f"""
STDOUT: {output.stdout}
STDERR: {output.stderr}
"""

        if output.stdout == "" and output.stderr == "":
            final_string = "No output produced.\n"

        if output.returncode != 0:
            final_string += f"Process exited with code {output.returncode}"
        return final_string
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
