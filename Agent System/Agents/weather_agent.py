# agents/weather_agent.py
import logging
from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend.chat import ChatModel
from google.adk.agents import Agent
from beeai_framework.backend.message import UserMessage
from beeai_framework.memory.token_memory import TokenMemory
from ..tools.tools import get_weather
from acp_protocol import ACPTransport  # Assuming ACP package for communication

# Initialize ACP Transport (if necessary)
acp_transport = ACPTransport()

# Weather Agent Definition
weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",  # Using the gemini-2.0-flash model
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "Only respond to queries about weather in specific cities. "
                "If the user specifies a city, use the 'get_weather' tool to retrieve the information. "
                "If no city is specified, politely ask the user to provide a city name. "
                "If the tool returns an error (e.g., city not found), inform the user politely that the weather for that city could not be retrieved and suggest trying another city. "
                "If the tool is successful, present the weather report clearly and concisely, including temperature, conditions, and any relevant details. "
                "Do not engage in unrelated conversations.",
    tools=[get_weather],
    transport=acp_transport,  # ACP transport for communication
)

# Define the server and message handler for weather_agent
server = Server()

@server.agent()
async def weather_agent_handler(inputs: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """Handles weather queries and responds using BeeAI and ACP"""
    
    # Create a llm instance
    llm = ChatModel.from_name("gemini-2.0-flash")  # Using the gemini-2.0-flash model

    # Create a memory instance
    memory = TokenMemory(llm)

    # Add messages to memory (simulate passing user messages to the memory)
    for message in inputs:
        await memory.add(UserMessage(str(message)))

    # Create ReActAgent with memory and tools
    agent = ReActAgent(llm=llm, tools=[get_weather], memory=memory)

    # Run the agent with memory to get a response
    response = await agent.run()

    # Yield the response to be sent via ACP
    yield MessagePart(content=response.result.text)

logging.info("weather_agent initialized with ACP transport")
