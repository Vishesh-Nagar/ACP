# Agent definitions and runners.

import logging
from .Agents.root_agent import root_agent as agent_team

root_agent = agent_team

# Log when agents are called
logging.info("weather_agent initialized")
logging.info("poem_agent initialized")
logging.info("translation_agent initialized")
logging.info("agent_team (root_agent) initialized")
