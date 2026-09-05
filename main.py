import os
import sys
import logging
from dotenv import load_dotenv

from agent import CodingAgent
from providers.gemini_provider import GeminiProvider
from config import Settings


def main():
    load_dotenv()

    if len(sys.argv) < 2:
        print("I need a prompt!")
        sys.exit(1)

    prompt = sys.argv[1]
    verbose_flag = len(sys.argv) == 3 and sys.argv[2] == "--verbose"

    logging.basicConfig(
        level=logging.DEBUG if verbose_flag else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    try:
        settings = Settings.from_env(working_directory=os.getcwd(), verbose=verbose_flag)
    except ValueError as e:
        print(f"Error: {e}")
        return

    provider = GeminiProvider(
        api_key=settings.gemini_api_key,
        model=settings.model,
        verbose=settings.verbose,
    )
    agent = CodingAgent(
        provider=provider,
        working_directory=settings.working_directory,
        max_iters=settings.max_iters,
        verbose=settings.verbose,
    )

    result = agent.run(prompt)
    print(result)


if __name__ == "__main__":
    main()