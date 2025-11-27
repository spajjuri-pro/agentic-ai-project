# My Agent — Google ADK Demo

A demo agent using Google's ADK (Agent Development Kit) with Vertex AI.

## Quick Start

### Prerequisites

- Python 3.9+, Google Cloud account with credits, gcloud CLI configured
- See [README-SETUP.md](./README-SETUP.md) for detailed setup instructions

### Run the agent

```bash
# Source the virtual environment
source .venv/bin/activate

# Build the ADK project
adk build

# Launch the web UI (port 8000)
adk web --port 8000

# In another terminal, activate venv and run the agent
source .venv/bin/activate
adk run my_agent
```

The web UI will be available at `http://localhost:8000`.

## File structure

- `agent.py` — Main agent definition
- `.env.example` — Template for environment variables (commit this, not `.env`)
- `.env` — Local credentials (do NOT commit)

## Docs

- [Setup Guide](./README-SETUP.md) — Full setup and credentials configuration
- [ADK docs](https://google.github.io/adk-docs/)
- [Vertex AI docs](https://cloud.google.com/vertex-ai/docs)
