import os
from dataclasses import dataclass

MAX_CHARS=10000

@dataclass
class Settings:
    gemini_api_key: str
    working_directory: str
    model: str = "gemini-3.6-flash"
    max_iters: int = 5
    max_chars: int = 10000
    verbose: bool = False

    @classmethod
    def from_env(cls, working_directory: str, verbose: bool = False) -> "Settings":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        return cls(gemini_api_key=api_key, working_directory=working_directory, verbose=verbose)