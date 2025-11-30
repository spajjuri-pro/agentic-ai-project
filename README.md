# My Agent — Google ADK Demo

A demo agent using Google's ADK (Agent Development Kit) with Vertex AI.

**AI Exercise Planner** — Personalized workout routines based on user profile and fitness goals, powered by a gym exercise database.

## Quick Start

### Prerequisites

- Python 3.9+, Google Cloud account with credits, gcloud CLI configured
- See [README-SETUP.md](./README-SETUP.md) for detailed setup instructions

### Run the agent

**Make sure you're in the parent directory** (`/Users/spajjuri`), NOT inside the `my_agent` folder.

**Option 1: Interactive CLI**
```bash
# From /Users/spajjuri (parent directory)
cd /Users/spajjuri

# Source the virtual environment
source my_agent/.venv/bin/activate

# Run the agent interactively
adk run my_agent
```

**Option 2: Web UI (port 8000)**
```bash
# From /Users/spajjuri (parent directory)
cd /Users/spajjuri

# Source the virtual environment
source my_agent/.venv/bin/activate

# Launch the web UI
adk web --port 8000
```

Then open `http://localhost:8000` in your browser.

## Agent Features

### Sequential Exercise Planner with Database

The agent follows a structured workflow to create personalized workout plans:

**Step 1: Collect & Save Profile**
- Gathers user information: name, age, height, weight, exercise goal, injuries
- Saves profile to local SQLite database (`user_profiles.db`)
- Returns profile ID for reference

**Step 2: Generate Personalized Plan**
- Retrieves the saved profile from database
- Generates personalized weekly workout plan based on:
  - **Fitness Goals**: Weight Loss, Strength Building, or Cardio
  - **User Profile**: Age, weight, height for difficulty adjustment
  - **Exercise Database**: Real exercises from `megaGymDataset.csv` (1000+ exercises)
  - **Injury Modifications**: Smart adjustments based on user limitations

**Step 3: Present Weekly Schedule**
- Monday-Sunday schedule organized by body part focus
- Specific exercises with equipment needed
- Difficulty level (Beginner, Intermediate, Advanced) based on age & weight
- Rest day recommendations and recovery guidance

### Database Architecture

Local SQLite database stores user profiles:
- `user_profiles.db` — User profiles with fitness goals and injury history
- Table: `user_profiles` (id, name, age, height, weight, exercise_goal, injury, created_at)
- Each user profile is persisted for future reference and plan updates

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
