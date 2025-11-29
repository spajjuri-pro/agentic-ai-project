# GitHub Copilot Instructions

## Project Overview

**agentic-ai-project** — A demo agent using Google's ADK (Agent Development Kit) with Vertex AI.

### Stack
- Python 3.9+
- Google Cloud (Vertex AI, ADK)
- gcloud CLI

### File Structure
- `agent.py` — Main agent (uses `google.adk.agents.llm_agent.Agent`)
- `__init__.py` — Package initialization
- `.env.example` — Safe template for env vars (commit this)
- `.env` — Local credentials (never commit, in `.gitignore`)
- `README.md` — Quick-start guide
- `README-SETUP.md` — Detailed setup and troubleshooting

## Code Style & Conventions

### Python
- **Format**: PEP 8, line length 88 chars (Black style)
- **Imports**: Alphabetical, grouped (stdlib, third-party, local)
- **Docstrings**: Google-style docstrings with Args, Returns sections
- **Type hints**: Use when practical for clarity
- **Naming**: `snake_case` for functions/vars, `PascalCase` for classes

### Example function:
```python
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.
    
    Args:
        city: The name of the city.
        
    Returns:
        A dictionary with status, city, and time.
    """
    return {"status": "success", "city": city, "time": "10:30 AM"}
```

## Commit Conventions

- **Format**: `<type>: <description>`
- **Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- **Examples**:
  - `feat: add retry backoff for 429 errors`
  - `fix: handle missing GOOGLE_APPLICATION_CREDENTIALS`
  - `docs: update setup instructions`
  - `refactor: simplify agent initialization`
  - `chore: format code and update .gitignore`

## Security & Environment

### Credentials
- **Never commit**: `.env`, `*.json` (service account keys), API keys
- **Use**: `GOOGLE_APPLICATION_CREDENTIALS` pointing to local service account file
- **For Vertex AI**: Service account required (API keys not supported)

### `.env` example:
```properties
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_APPLICATION_CREDENTIALS=~/adk-agent-sa-key.json
```

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| 401 UNAUTHENTICATED | Using API key with Vertex AI | Use service account (`.env` setup) |
| 429 RESOURCE_EXHAUSTED | Quota exhausted or billing disabled | Enable billing, check [ai.dev/usage](https://ai.dev/usage), or switch models |
| ModuleNotFoundError | Missing dependencies | Run `pip install google-adk google-cloud-aiplatform` |

## Testing & Running

```bash
# Activate venv
source .venv/bin/activate

# Format & lint
black agent.py __init__.py
flake8 agent.py __init__.py

# Run agent interactively
adk run my_agent

# Run agent with web UI (port 8000)
adk web --port 8000
```

## When Making Changes

1. **Before editing**: Ensure you understand the Google ADK API and Vertex AI requirements
2. **Code quality**: Keep functions small, use type hints, write clear docstrings
3. **Testing**: Test locally with `adk build && adk run my_agent` before committing
4. **Docs**: Update `README.md` or `README-SETUP.md` if behavior changes
5. **Secrets**: Never add credentials to code; use `.env` and `.gitignore`

## Useful Resources

- [ADK Docs](https://google.github.io/adk-docs/)
- [Vertex AI Docs](https://cloud.google.com/vertex-ai/docs)
- [Google Cloud Authentication](https://cloud.google.com/docs/authentication)
- [Rate Limits & Quotas](https://ai.google.dev/gemini-api/docs/rate-limits)
