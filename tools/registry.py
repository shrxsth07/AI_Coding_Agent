from Functions.get_files_info import get_files_info, schema_get_files_info
from Functions.get_file_content import get_file_content, schema_get_file_content
from Functions.write_file import write_file, schema_write_file
from Functions.run_python_file import run_python_file, schema_run_python_file

# Each entry: tool name -> (actual function, its Gemini schema declaration)
TOOL_REGISTRY = {
    "get_files_info": (get_files_info, schema_get_files_info),
    "get_file_content": (get_file_content, schema_get_file_content),
    "write_file": (write_file, schema_write_file),
    "run_python_file": (run_python_file, schema_run_python_file),
}


def get_all_schemas():
    """Returns the list of schemas for every registered tool — used to build
    the Tool declaration sent to the LLM provider."""
    return [schema for _, schema in TOOL_REGISTRY.values()]