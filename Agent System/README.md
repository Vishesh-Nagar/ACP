# Agent Team Assistant

This project implements a multi-agent assistant system using Google ADK (Agent Development Kit). The system features a team of specialized agents that handle weather queries, poem requests, greetings, and farewells.

## Project Structure

The project is organized into modular components for better maintainability and scalability:

```
agent_team/
├── README.md              # This file
├── .env                   # Environment variables (API keys)
├── .gitignore             # Git ignore rules
├── .venv/                 # Virtual environment
├── config.py              # Configuration, imports, and constants
├── tools.py               # Tool function definitions
├── agents.py              # Agent definitions and configurations
├── sessions.py            # Session service setup and management
├── interactions.py        # Interaction functions and conversation logic
├── main.py                # Main entry point
├── main.ipynb             # Jupyter notebook version with examples
├── requirements.txt       # Python dependencies
└── __pycache__/           # Python cache files
```

## File Descriptions

### config.py
- **Purpose**: Handles initial setup, library imports, API key configuration, and model constants.
- **Key Components**:
  - Google ADK imports
  - API key setup (Google Gemini)
  - Model constants (e.g., `MODEL_GEMINI_2_0_FLASH`)
  - Warning suppression and logging configuration

### tools.py
- **Purpose**: Defines all tool functions used by agents.
- **Key Components**:
  - `get_weather()`: Weather retrieval tool using WeatherAPI.com for real weather data
  - `say_hello()`: Greeting tool with optional name parameter
  - `say_goodbye()`: Farewell tool

### agents.py
- **Purpose**: Contains all agent definitions and configurations.
- **Key Components**:
  - `weather_agent`: Specialized agent for weather queries
  - `poem_agent`: Specialized agent for poem requests
  - `agent_team`: Root agent coordinating sub-agents for weather, poems, greetings, and farewells

### sessions.py
- **Purpose**: Manages session services and runners.
- **Key Components**:
  - `InMemorySessionService` setup
  - Session creation and runner initialization

### interactions.py
- **Purpose**: Handles user-agent interactions asynchronously.
- **Key Components**:
  - `call_agent_async()`: Core function for sending queries to agents
  - `run_conversation()`: Interactive conversation loop

### main.py
- **Purpose**: Main entry point for the application.
- **Function**: Runs the interactive conversation with the agent team.

### main.ipynb
- **Purpose**: Jupyter notebook with comprehensive examples and tutorials.
- **Function**: Demonstrates various agent configurations, tools, and conversation scenarios.

## System Initialization Flow

1. **Configuration Loading** (`config.py`):
   - Import required libraries
   - Set up API keys and environment variables
   - Define model constants
   - Configure logging and warnings

2. **Tool Definition** (`tools.py`):
   - Define tool functions with their logic
   - Tools are loaded into memory for agent use

3. **Session Setup** (`sessions.py`):
   - Initialize `InMemorySessionService`
   - Create sessions with optional initial state
   - Set up session identifiers (app_name, user_id, session_id)

4. **Agent Creation** (`agents.py`):
   - Define individual agents with their tools and instructions
   - Create sub-agents for specialized tasks
   - Build root agents that coordinate sub-agents
   - Apply guardrails and state management

5. **Runner Initialization**:
   - Create `Runner` instances linking agents to session services
   - Prepare for asynchronous execution

## Data Flow

### User Query Processing:
1. User query → `call_agent_async()` in `interactions.py`
2. Query formatted into ADK `Content` object
3. Runner executes agent logic asynchronously
4. Agent processes query through:
   - **Model Call**: LLM generates response (potentially intercepted by guardrails)
   - **Tool Execution**: If needed, tools are called (potentially blocked by guardrails)
   - **Sub-agent Delegation**: Root agent may delegate to specialized sub-agents
5. Final response returned to user

### State Management:
- Session state persists across interactions
- Tools can read/write state (e.g., user preferences, last actions)
- Guardrails can modify state (e.g., trigger flags)
- State is stored in `InMemorySessionService`

### Guardrail Flow:
- **Input Guardrail** (`before_model_callback`): Checks user input before LLM call
- **Tool Guardrail** (`before_tool_callback`): Validates tool arguments before execution
- If guardrail triggers, returns predefined response instead of proceeding

## Overall System Function

The system operates as a conversational AI assistant with the following capabilities:

1. **Weather Information**: Provides real-time weather reports for cities using WeatherAPI.com
2. **Poem Generation**: Creates or recites poems based on user requests
3. **Greetings and Farewells**: Handles polite interactions using dedicated tools
4. **Multi-Agent Coordination**: Delegates tasks to specialized sub-agents (weather_agent, poem_agent)

### Key Features:
- Asynchronous execution using `asyncio`
- Modular agent architecture with sub-agent delegation
- Real weather data integration via API
- Interactive conversation loop in the terminal
- Extensible tool system for adding new capabilities

## Usage

### Running the System:
```bash
cd agent_team
python main.py
```

### Configuration:
- Set your Google API key in `.env` file (GOOGLE_API_KEY)
- Set your WeatherAPI key in `.env` file (WEATHERAPI_KEY)
- Adjust model constants in `config.py` for different LLM providers
- Modify tool logic in `tools.py` for custom integrations

## Dependencies

See `requirements.txt` for Python package requirements. Key dependencies:
- `google-adk`: Agent Development Kit
- `google-genai`: Google Generative AI library

## Testing

The system can be tested by running the interactive conversation loop and trying various queries:
- Weather queries: "What's the weather in London?"
- Poem requests: "Can you recite a poem?"
- Greetings: "Hello" or "Hi there"
- Farewells: "Goodbye" or "See you later"

## Future Enhancements

- Add more specialized sub-agents for additional tasks
- Implement persistent storage for conversation history
- Add user authentication and multi-user support
- Expand capabilities with more tools and integrations
