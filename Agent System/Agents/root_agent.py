# agents/agent_team.py
import logging
from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from google.adk.agents import Agent
from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend.chat import ChatModel
from beeai_framework.backend.message import UserMessage
from beeai_framework.memory.token_memory import TokenMemory
from .weather_agent import weather_agent
from .poem_agent import poem_agent
from .translation_agent import translation_agent
from ..tools.tools import say_hello
from acp_protocol import ACPTransport  # Assuming ACP package for communication

# Initialize ACP Transport
acp_transport = ACPTransport()

# Main Agent Team (Root Agent)
agent_team = Agent(
    name="agent_team",
    model="gemini-2.0-flash",  # Using the gemini-2.0-flash model
    description="The main coordinator agent. Handles greetings and farewell prompts and delegates requests to specialists.",
    instruction="You are the main Agent coordinating a team. "
                "Your primary responsibility is to handle greetings using the 'say_hello' tool. "
                "You have three specialized sub-agents: weather_agent for weather queries, poem_agent for poem requests, and translation_agent for English-to-Spanish translations. "
                "Analyze the user's query carefully. "
                "If the query is a greeting (e.g., hello, hi), use 'say_hello'. "
                "If the query is about weather in a city, delegate to the weather_agent by passing the query. "
                "If the query requests a poem, delegate to the poem_agent. "
                "If the query is a translation from English to Spanish, delegate to the translation_agent. "
                "For any other query, respond politely that you can assist with greetings, weather, poems, or translations, and ask how you can help. "
                "Do not handle the delegated tasks yourself; always delegate to the appropriate sub-agent.",
    tools=[say_hello],
    sub_agents=[weather_agent, poem_agent, translation_agent],
    transport=acp_transport,  # ACP transport for communication
)

# Define the server and message handler for agent_team (root agent)
server = Server()

@server.agent()
async def agent_team_handler(inputs: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """Handles agent team coordination and delegates tasks to sub-agents"""
    
    # Create a llm instance
    llm = ChatModel.from_name("gemini-2.0-flash")  # Using the gemini-2.0-flash model

    # Create a memory instance
    memory = TokenMemory(llm)

    # Add messages to memory (simulate passing user messages to the memory)
    for message in inputs:
        await memory.add(UserMessage(str(message)))

    # Create ReActAgent with memory and sub-agents
    agent = ReActAgent(llm=llm, tools=[say_hello], memory=memory)

    # Run the agent with memory to get a response
    response = await agent.run()

    # Yield the response to be sent via ACP
    yield MessagePart(content=response.result.text)

logging.info("agent_team (root_agent) initialized with ACP transport")
