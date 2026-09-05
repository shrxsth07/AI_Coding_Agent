import os
import sys
from dotenv import load_dotenv

from agent import CodingAgent


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set.")
        return

    if len(sys.argv) < 2:
        print("I need a prompt!")
        sys.exit(1)

    prompt = sys.argv[1]
    verbose_flag = len(sys.argv) == 3 and sys.argv[2] == "--verbose"

    # The directory from which the agent is being executed.
    # All file operations are restricted to this directory.
    working_directory = os.getcwd()

    agent = CodingAgent(
        api_key=api_key,
        working_directory=working_directory,
        verbose=verbose_flag,
    )

    result = agent.run(prompt)
    print(result)


if __name__ == "__main__":
    main()