import logging
from ..config import MODEL
from google.adk.agents import Agent
from ..tools import say_hello
from .weather_agent import weather_agent
from .poem_agent import poem_agent
from .translation_agent import translation_agent

root_agent = Agent(
    name="root_agent",
    model=MODEL,
    description="The main coordinator agent. Handles greetings and delegates requests to specialists.",
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
)
