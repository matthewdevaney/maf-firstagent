import asyncio

from agent_framework import (
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    executor,
    handler
)

from typing_extensions import Never

""" First Workflow - Chain Executors with edges

This sample builds a minimal workflow with two steps:
1. Covert text to uppercase (class-based executor)
2. Reverse the text (function-based executor)

No external services required
"""

def main() -> None:
    pass


if __name__ == "__main__":
    asyncio.run(main())