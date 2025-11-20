# agents/poem_agent.py
import logging
from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from beeai_framework.agents.react import ReActAgent
from google.adk.agents import Agent
from beeai_framework.backend.chat import ChatModel
from beeai_framework.backend.message import UserMessage
from beeai_framework.memory.token_memory import TokenMemory
from acp_protocol import ACPTransport  # Assuming ACP package for communication

# Initialize ACP Transport (if necessary)
acp_transport = ACPTransport()

# Poem Agent Definition
poem_agent = Agent(
    name="poem_agent",
    model="gemini-2.0-flash",  # Using the gemini-2.0-flash model
    description="Recites poems upon user request.",
    instruction="You are a poetic assistant. "
                "Only respond to requests for poems, including haikus, sonnets, or any poetic form. "
                "If the user requests a poem, provide one that is relevant to any themes, topics, or emotions mentioned. "
                "If no specific theme is given, create an original poem on a positive or inspirational topic. "
                "Ensure the response is solely the poem, without additional commentary unless necessary. "
                "If the request is not for a poem, do not respond.",
    tools=[],
    transport=acp_transport,  # ACP transport for communication
)

# Define the server and message handler for poem_agent
server = Server()

@server.agent()
async def poem_agent_handler(inputs: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """Handles poem requests and responds using BeeAI and ACP"""
    
    # Create a llm instance
    llm = ChatModel.from_name("gemini-2.0-flash")  # Using the gemini-2.0-flash model

    # Create a memory instance
    memory = TokenMemory(llm)

    # Add messages to memory (simulate passing user messages to the memory)
    for message in inputs:
        await memory.add(UserMessage(str(message)))

    # Create ReActAgent with memory
    agent = ReActAgent(llm=llm, tools=[], memory=memory)

    # Run the agent with memory to get a response
    response = await agent.run()

    # Yield the response to be sent via ACP
    yield MessagePart(content=response.result.text)

logging.info("poem_agent initialized with ACP transport")
