# Main entry point for the agent team application

from .config.config import *
from .tools.tools import *
from .agents import *
from .sessions import *
from .interactions.interactions import *

if __name__ == "__main__":
    asyncio.run(run_conversation())
