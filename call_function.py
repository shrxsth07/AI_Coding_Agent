from tools.registry import TOOL_REGISTRY


def call_function(tool_call, working_directory, verbose=False):
    if verbose:
        print(f"Calling function: {tool_call.name}({tool_call.args})")
    else:
        print(f" - Calling function: {tool_call.name}")

    entry = TOOL_REGISTRY.get(tool_call.name)
    if entry is None:
        return f"Unknown function: {tool_call.name}"

    function, _schema = entry
    return function(working_directory, **tool_call.args)