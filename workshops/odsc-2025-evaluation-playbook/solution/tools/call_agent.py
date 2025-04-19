import asyncio
from functools import wraps

import click

from evaluation_playbook.workflow import agent


def async_command(f):
    """Decorator to run an async click command."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@click.option(
    "--philosopher-id",
    type=str,
    required=True,
    help="ID of the philosopher to call.",
)
@click.option(
    "--query",
    type=str,
    required=True,
    help="Query to call the agent with.",
)
@async_command
async def main(philosopher_id: str, query: str) -> None:
    """CLI command to create long-term memory for philosophers.

    Args:
        philosopher_id: ID of the philosopher to call.
        query: Query to call the agent with.
    """

    agent.render_graph()

    print(
        f"\033[32mCalling agent with philosopher_id: `{philosopher_id}` and query: `{query}`\033[0m"
    )
    print("\033[32mResponse:\033[0m")
    print("\033[32m--------------------------------\033[0m")
    async for chunk in agent.stream(
        messages=query,
        philosopher_id=philosopher_id,
    ):
        print(f"\033[32m{chunk}\033[0m", end="", flush=True)
    print("\033[32m--------------------------------\033[0m")


if __name__ == "__main__":
    main()
