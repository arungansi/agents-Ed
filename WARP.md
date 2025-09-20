# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is the "Master AI Agentic Engineering" course codebase - a comprehensive 6-week journey to build autonomous AI agents using OpenAI Agents SDK, CrewAI, LangGraph, AutoGen and MCP (Model Context Protocol). The course covers foundations, advanced frameworks, and practical implementations of agentic AI systems.

## Development Environment Setup

### Package Management
The project uses **uv** (the blazingly fast Python package manager) for dependency management:

```bash
# Install dependencies
uv sync

# Add new packages
uv add package_name

# Run scripts (preferred over direct python calls)
uv run script_name.py

# Update all packages
uv lock --upgrade

# Install CrewAI tool for week 3
uv tool install crewai
uv tool upgrade crewai
```

### Python Version
- Requires Python 3.12 (specified in `.python-version`)
- Virtual environment managed by uv in `.venv/`

## Key Frameworks & Architecture

### Core Technologies Stack
- **OpenAI Agents SDK**: For basic agents and hosted tools (WebSearchTool, FileSearchTool, ComputerTool)
- **LangGraph**: State-based agent workflows with graph execution
- **AutoGen**: Multi-agent orchestration and collaboration
- **CrewAI**: Role-based agent teams and specialized workflows
- **MCP (Model Context Protocol)**: Standardized tool integration and data sharing
- **Anthropic Claude**: Alternative LLM provider
- **Gradio**: Web interfaces for agent applications

### Directory Structure & Frameworks

#### `1_foundations/`
- Basic agent patterns and Gradio web interfaces
- Personal assistant implementations
- Entry-level agentic concepts
- **Key files**: `app.py` (Gradio chatbot with tool integration)

#### `2_openai/`
- OpenAI Agents SDK implementations
- Web search and research agents
- Structured outputs with Pydantic
- **Key patterns**: WebSearchTool usage, multi-agent research systems

#### `3_crew/`
- CrewAI implementations with specialized teams:
  - `coder/`: Development team agents
  - `debate/`: Debate and discussion agents
  - `engineering_team/`: Technical team coordination
  - `financial_researcher/`: Financial analysis agents
  - `stock_picker/`: Investment research agents

#### `4_langgraph/`
- State-based agent workflows
- **Key files**: 
  - `sidekick.py`: Main LangGraph implementation with worker/evaluator pattern
  - `sidekick_tools.py`: Tool definitions and browser automation
  - `app.py`: Gradio interface for LangGraph agents

#### `5_autogen/`
- Multi-agent systems with AutoGen
- **Key patterns**: RoutedAgent implementations, message handling
- **Key files**: 
  - `agent.py`: Base agent with creative entrepreneur persona
  - `messages.py`: Message routing and handling
  - `world.py`: Agent world coordination

#### `6_mcp/`
- Model Context Protocol implementations
- **Key components**: 
  - Trading floor simulation with multiple agents
  - Server/client architectures (`*_server.py`, `*_client.py`)
  - Database integration and persistence

## Common Development Commands

### Running Applications
```bash
# Run Gradio applications
uv run 1_foundations/app.py
uv run 4_langgraph/app.py

# Run Jupyter notebooks
jupyter notebook  # or use Cursor/VS Code

# Run CrewAI projects (from project directories)
crewai run
```

### Testing & Development
```bash
# Run diagnostics
uv run setup/diagnostics.py

# Reset databases (for MCP section)
uv run 6_mcp/reset.py

# Install Playwright for browser automation
uv run playwright install
```

## Architecture Patterns

### Agent Communication Patterns
1. **Direct Tool Usage**: Agents directly call tools and APIs
2. **Handoff Pattern**: Agents pass work to specialized agents (OpenAI SDK)
3. **State Management**: LangGraph manages conversation state and routing
4. **Message Broadcasting**: AutoGen agents communicate via message system
5. **MCP Integration**: Standardized tool and data source connections

### Key Design Principles
- **Modular Architecture**: Each framework demonstrates different agent patterns
- **Tool Integration**: Extensive use of external APIs and browser automation
- **State Persistence**: Database storage for complex workflows
- **Evaluation Systems**: Built-in success criteria and feedback loops (LangGraph)
- **Multi-Modal**: Support for text, file processing, and web interactions

## Environment Variables Required

Create a `.env` file in the project root with:
```env
OPENAI_API_KEY=sk-proj-...
GOOGLE_API_KEY=...              # For Gemini integration
ANTHROPIC_API_KEY=...           # For Claude integration
GEMINI_API_KEY=...              # Alias for Google API (CrewAI requirement)
PUSHOVER_TOKEN=...              # For notifications
PUSHOVER_USER=...               # For notifications
SENDGRID_API_KEY=...            # For email functionality
```

## Tool Ecosystem

### Web & Browser Tools
- **WebSearchTool**: OpenAI's hosted web search (costs ~$0.025/call)
- **Playwright**: Browser automation for complex web interactions
- **Beautiful Soup**: HTML parsing and web scraping

### AI & LLM Tools
- **OpenAI Models**: gpt-4o, gpt-4o-mini primary models
- **Anthropic Claude**: Alternative high-performance LLM
- **Google Gemini**: Cost-effective alternative
- **Ollama**: Local LLM hosting (free alternative)

### Data & File Tools
- **PDF Processing**: pypdf, pypdf2 for document handling
- **Database**: SQLite for persistence (LangGraph, MCP)
- **Structured Outputs**: Pydantic models for type-safe AI responses

### Communication Tools
- **Email**: SendGrid integration
- **Notifications**: Pushover for mobile alerts
- **Web Interfaces**: Gradio for rapid prototyping

## Development Workflow

### Course Progression Pattern
1. **Week 1-2**: Foundation concepts and basic agents
2. **Week 3**: CrewAI team-based agents
3. **Week 4**: LangGraph state management
4. **Week 5**: AutoGen multi-agent systems
5. **Week 6**: MCP protocol and advanced integrations

### Agent Development Best Practices
- Use structured outputs (Pydantic) for reliable AI responses
- Implement proper error handling and fallbacks
- Design clear success criteria for agent evaluation
- Leverage existing tool ecosystem rather than building from scratch
- Test with cost-effective models before scaling to production

## Common Issues & Solutions

### API Costs
- OpenAI WebSearchTool costs ~$0.025 per call
- Monitor usage at https://platform.openai.com/usage
- Use alternatives like free web scraping or Ollama for development

### CrewAI Setup (Windows)
- Requires Microsoft Build Tools installation
- May need `$env:PYTHONUTF8 = "1"` for Unicode issues
- Use `uv tool install crewai` for proper installation

### Environment Issues
- Disable Anaconda auto-activation: `conda config --set auto_activate_base false`
- Use `uv --native-tls sync` for certificate issues
- Ensure `.env` file is exactly named (not `.env.txt`)

## Production Considerations

### Security
- Never commit API keys or sensitive data
- Use environment variables for all credentials
- Monitor API usage and set spending limits

### Scaling
- Agent systems are less predictable than traditional software
- Implement proper logging and tracing (OpenAI traces available)
- Design for graceful degradation when external services fail
- Consider rate limiting for production deployments

### Performance
- Cache frequently accessed data
- Use appropriate model sizes (gpt-4o-mini vs gpt-4o)
- Implement proper connection pooling for database access
- Consider async patterns for concurrent agent operations