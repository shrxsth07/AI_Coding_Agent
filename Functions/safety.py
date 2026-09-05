import os


class PathTraversalError(Exception):
    """Raised when a requested path would escape the working directory."""


def resolve_safe_path(working_directory: str, relative_path: str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, relative_path))

    if abs_target != abs_working_dir and not abs_target.startswith(abs_working_dir + os.sep):
        raise PathTraversalError(f'"{relative_path}" is not in the working directory')

    return abs_target