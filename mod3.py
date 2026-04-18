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





# Run Agent

async def main() -> None:
    # create client
    client = FoundryChatClient(
        project_endpoint="https://maf-foundry-20260417.services.ai.azure.com/api/projects/proj-default",
        model="gpt-5.3-chat",
        credential=AzureCliCredential()
    )

    #create agent
    agent = Agent(
        client=client,
        name="ConversationAgent",
        instructions="You are a friendly assistant. Keep your answers brief"
    )

    # create session
    session = agent.create_session()

    # message 1
    print("\n")
    print("Agent: Tell me a fact about yourself.\n")
    user_message = input("User: ")
    print("\n")
    result = await agent.run(user_message, session=session)
    print(f"Agent: {result}\n")

    # message 2
    user_message = "What do you remember about me?"
    print(f"User: {user_message}\n")
    result = await agent.run(user_message, session=session)
    print(f"Agent: {result}\n")

    """
    async for chunk in agent.run(user_message, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()
    """

if __name__ == "__main__":
    asyncio.run(main())