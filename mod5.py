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

# class-based executor that converts text to uppercase
class UpperCase(Executor):
    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        """Convert input to uppercase and forward to the next node"""
        await ctx.send_message(text.upper())

# function-based executor that reverses the string and yields output
@executor(id="reverse_text")
async def reverse_text(text:str, ctx: WorkflowContext[Never, str]) -> None:
    """Reverse the string and yield the final workflow output"""
    await ctx.yield_output(text[::-1])

def create_workflow():
    """Build the workflow: Uppercase -> reverse_text"""
    upper = UpperCase(id="upper_case")
    return WorkflowBuilder(start_executor=upper).add_edge(upper, reverse_text).build()


def main() -> None:
    pass


if __name__ == "__main__":
    asyncio.run(main())