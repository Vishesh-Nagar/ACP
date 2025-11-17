import logging
from ..config import MODEL
from google.adk.agents import Agent
from ..tools import get_weather

weather_agent = Agent(
    name="weather_agent",
    model=MODEL,
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "Only respond to queries about weather in specific cities. "
                "If the user specifies a city, use the 'get_weather' tool to retrieve the information. "
                "If no city is specified, politely ask the user to provide a city name. "
                "If the tool returns an error (e.g., city not found), inform the user politely that the weather for that city could not be retrieved and suggest trying another city. "
                "If the tool is successful, present the weather report clearly and concisely, including temperature, conditions, and any relevant details. "
                "Do not engage in unrelated conversations.",
    tools=[get_weather],
)
