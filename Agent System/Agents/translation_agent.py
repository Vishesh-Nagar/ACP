# agents/translation_agent.py
import logging
from acp_sdk.models import Message, MessagePart
from google.adk.agents import Agent
from acp_sdk.server import RunYield, RunYieldResume, Server
from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend.chat import ChatModel
from beeai_framework.backend.message import UserMessage
from collections.abc import AsyncGenerator
from ..tools.tools import translate_english_to_spanish
from beeai_framework.memory.token_memory import TokenMemory
from acp_sdk.transport import ACPTransport

# Initialize ACP Transport (if necessary)
acp_transport = ACPTransport()

# Translation Agent Definition
translation_agent = Agent(
    name="translation_agent",
    model="gemini-2.0-flash",  # Using the gemini-2.0-flash model
    description="Translates English sentences to Spanish.",
    instruction="You are a translation assistant. "
                "Only handle requests to translate English text to Spanish. "
                "If the user provides an English sentence or phrase, use the 'translate_english_to_spanish' tool to attempt the translation. "
                "If the tool indicates that the translation is incomplete (e.g., some words not translated), use your knowledge to complete the translation accurately. "
                "Provide only the Spanish translation as the response, without any additional commentary. "
                "If the input is not in English or not a translation request, inform the user politely that you can only translate English to Spanish.",
    tools=[translate_english_to_spanish],
    transport=acp_transport,  # ACP transport for communication
)

# Define the server and message handler for translation_agent
server = Server()

@server.agent()
async def translation_agent_handler(inputs: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """Handles translation requests and responds using BeeAI and ACP"""
    
    # Create a llm instance
    llm = ChatModel.from_name("gemini-2.0-flash")  # Using the gemini-2.0-flash model

    # Create a memory instance
    memory = TokenMemory(llm)

    # Add messages to memory (simulate passing user messages to the memory)
    for message in inputs:
        await memory.add(UserMessage(str(message)))

    # Create ReActAgent with memory and tools
    agent = ReActAgent(llm=llm, tools=[translate_english_to_spanish], memory=memory)

    # Run the agent with memory to get a response
    response = await agent.run()

    # Yield the response to be sent via ACP
    yield MessagePart(content=response.result.text)

logging.info("translation_agent initialized with ACP transport")
