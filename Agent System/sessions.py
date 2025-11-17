# Session management and runners for agents.

import asyncio
import logging
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from .agents import agent_team

session_service = InMemorySessionService()

APP_NAME = "agent_team"
USER_ID = "user_1"
SESSION_ID = "session_001"

async def setup_session():
    global session
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

# Runner will be created after agents are imported
runner = Runner(agent=agent_team, session_service=session_service, app_name=APP_NAME)

logging.info("session_service and runner initialized")
