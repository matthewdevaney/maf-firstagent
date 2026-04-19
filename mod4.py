import asyncio
from typing import Any

from agent_framework import Agent, AgentSession, ContextProvider, SessionContext
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

"""
Agent Memory with Context Providers and Session State

Context providers inject dynamic context into each agent call. This sample
shows a provider that stores the user's name in session state and personalizes
responses — the name persists across turns via the session.
"""


class UserMemoryProvider(ContextProvider):
    """A context provider that remembers user info in session state"""

    DEFAULT_SOURCE_ID = "user_memory"

    def __init__(self):
        super().__init__(self.DEFAULT_SOURCE_ID)

    async def before_run(
        self,
        *,
        agent: Any,
        session: AgentSession | None,
        context: SessionContext,
        state: dict[str, Any]
    ) -> None:
        """Inject personalization instructions based on stored user info"""
        user_name = state.get("user_name")
        if user_name:
            context.extend_instructions(
                self.source_id,
                f"The user's name is {user_name}. Always address them by name."
            )
        else:
            context.extend_instructions(
                self.source_id,
                "You don't know the user's name yet. Ask for it politely."
            )

    async def after_run(
        self,
        *,
        agent: Any,
        session: AgentSession | None,
        context: SessionContext,
        state: dict[str, any]
    ) -> None:
        
        """Extract and store user info in session state after each call"""
        for msg in context.input_messages:
            text = msg.text if hasattr(msg, "text") else ""
            if isinstance(text, str) and "my name is" in text.lower():
                state["user_name"] = text.lower().split("my name is")[-1].strip().split()[0].capitalize()

async def main():

    client = FoundryChatClient(
        project_endpoint="https://maf-foundry-20260417.services.ai.azure.com/api/projects/proj-default",
        model="gpt-5.3-chat",
        credential=AzureCliCredential()
    )

    agent = Agent(
        client=client,
        name="MemoryAgent",
        instructions="You are a friendly assistant.",
        context_providers=[UserMemoryProvider()]
    )

    session = agent.create_session()

    # The provider doesn't know the user yet - it will ask for a name
    user_message = "Hello! What's the square root of 9?"
    print(f"User: {user_message}\n")
    result = await agent.run(
        user_message,
        session=session
    )
    print(f"Agent: {result}\n")

    # Now provide the name = the provider stores it in session state
    user_message = "My name is Alice"
    print(f"User: {user_message}\n")
    result = await agent.run(
        user_message,
        session=session
    )
    print(f"Agent: {result}\n")

    # Subsequent calls are personalized - name persists via session starts
    user_message = "What is 2 + 2"
    print(f"User: {user_message}\n")
    result = await agent.run(
        user_message,
        session=session
    )
    print(f"Agent: {result}\n")

    # Inspect session state to see what the provider stored
    provider_state = session.state.get("user_memory", {})
    print(f"[Session State] Stored user name: {provider_state.get('user_name')}")

if __name__ == "__main__":
    asyncio.run(main())