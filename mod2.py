import asyncio
from random import randint
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import Field


#Define Agent Tools"""

@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0,3)]} with a high of {randint(10,30)}°C."


# Create Agent

client = FoundryChatClient(
    project_endpoint="https://maf-foundry-20260417.services.ai.azure.com/api/projects/proj-default",
    model="gpt-5.3-chat",
    credential=AzureCliCredential()
)

agent = Agent(
    client=client,
    name="HelloAgent",
    instructions="You are a heplful weather agent. Use the get_weather tool to answer questions.",
    tools=[get_weather]
)


## Run Agent

async def main():
    user_message = input("Ask the weather agent a question: ")
    # Streaming: receive tokens as they are generated
    # print("Agent (streaming): ", end="", flush=True)
    async for chunk in agent.run(user_message, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
print()

if __name__ == "__main__":
    asyncio.run(main())