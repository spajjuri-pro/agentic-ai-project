# My Agent — Google ADK Demo

A demo agent using Google's ADK (Agent Development Kit) with Vertex AI.

**AI Exercise Planner** — Personalized workout routines based on user profile and fitness goals, powered by a gym exercise database.

## Quick Start

### Prerequisites

- Python 3.9+, Google Cloud account with credits, gcloud CLI configured
- See [README-SETUP.md](./README-SETUP.md) for detailed setup instructions

### Run the agent

**Option 1: Interactive CLI**
```bash
# Source the virtual environment
source .venv/bin/activate

# Run the agent interactively
adk run my_agent
```

**Option 2: Web UI (port 8000)**
```bash
# Source the virtual environment
source .venv/bin/activate

# Launch the web UI
adk web --port 8000
```

Then open `http://localhost:8000` in your browser.

## Agent Features

### Exercise Planner
The agent collects user information and generates personalized weekly workout plans:
- **User Input**: First name, last name, age, injury/limitations, height, weight
- **Fitness Goals**: Weight Loss, Strength Building, Cardio (Stamina)
- **Weekly Schedule**: Personalized routine organized by day with specific exercises
- **Exercise Database**: Real exercises from `megaGymDataset.csv` (1000+ exercises)
- **Injury Modifications**: Smart adjustments based on user limitations
- **User Feedback**: Collects feedback after workout recommendations

## File structure

- `agent.py` — Exercise Planner agent with CSV filtering tools
- `megaGymDataset.csv` — Database of 1000+ gym exercises (body parts, equipment, difficulty)
- `.env.example` — Template for environment variables (commit this, not `.env`)
- `.env` — Local credentials (do NOT commit)

## Example Usage

```
User: Give me an exercise plan
Agent: I need some information about you...
  - First Name? → Shashi
  - Last Name? → P
  - Age? → 50
  - Any injuries? → Knee injury
  - Height? → 5'2"
  - Weight? → 175 lbs
  - Goal? → Weight Loss

Agent: ✅ Here's your personalized weekly workout plan...
  Monday: Cardio & Abdominals
  Tuesday: Leg exercises
  Wednesday: Rest
  Thursday: Back exercises
  Friday: Chest exercises
  ...

Agent: Did you like these exercises?
```

## Docs

- [Setup Guide](./README-SETUP.md) — Full setup and credentials configuration
- [ADK docs](https://google.github.io/adk-docs/)
- [Vertex AI docs](https://cloud.google.com/vertex-ai/docs)
