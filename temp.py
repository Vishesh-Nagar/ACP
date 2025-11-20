from typing import Annotated
import os
from typing_extensions import TypedDict
from dotenv import load_dotenv

# ACP SDK
from acp_sdk.models import Message
from acp_sdk.models.models import MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from collections.abc import AsyncGenerator

# Langchain SDK
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


# Set up the AI model of your choice
llm = ChatAnthropic(
    model="claude-3-5-sonnet-latest", api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# ------ACP Requirement-------#
# START SERVER
server = Server()


# WRAP AGENT IN DECORACTOR
@server.agent()
async def chatbot(messages: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    "A simple chatbot enabled with memory"
    # formats ACP Message format to be compatible with what langchain expects
    query = " ".join(part.content for m in messages for part in m.parts)
    # invokes llm
    llm_response = llm.invoke(query)
    # formats langchain response to ACP compatible output
    assistant_message = Message(parts=[MessagePart(content=llm_response.content)])
    # Yield so add_messages merges it into state
    yield {"messages": [assistant_message]}


server.run()
# ---------------------------#
