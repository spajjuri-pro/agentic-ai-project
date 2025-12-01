# My Agent — Google ADK Demo

A demo agent using Google's ADK (Agent Development Kit) with Vertex AI.

**AI Exercise Planner** — Personalized workout routines based on user profile and fitness goals, powered by a gym exercise database.

---

## 📖 Documentation Guide

**👤 For End Users (Using the Application):**

- **[USER_README.md](./USER_README.md)** — Complete user guide with examples and FAQs
- **[WEB_UI_GUIDE.md](./WEB_UI_GUIDE.md)** — How to use the web interface

**👨‍💻 For Developers (Setting Up & Maintaining):**

- **[README-SETUP.md](./README-SETUP.md)** — Installation, configuration, and troubleshooting
- **[AGENT_DISCOVERY_FIX.md](./AGENT_DISCOVERY_FIX.md)** — Technical explanation of agent discovery
- **[DOCUMENTATION_UPDATE_SUMMARY.md](./DOCUMENTATION_UPDATE_SUMMARY.md)** — Project changes overview
- **[DOCUMENTATION_CHECKLIST.md](./DOCUMENTATION_CHECKLIST.md)** — Development verification

---

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

```
my_agent/
├── my_agent_app/           ← Agent package (ADK discovery point)
│   ├── __init__.py         ← Exports root_agent
│   ├── agent.py            ← Exercise Planner agent with CSV filtering tools
│   ├── megaGymDataset.csv  ← Database of 1000+ gym exercises
│   └── user_profiles.db    ← SQLite database for user profiles
├── __init__.py             ← Root package exports
├── .env                    ← Local credentials (do NOT commit)
├── .env.example            ← Template for environment variables
├── README.md               ← This file
└── README-SETUP.md         ← Detailed setup instructions
```

**Why the subdirectory?** ADK discovers agents by looking for package directories (folders with `__init__.py`). The `my_agent_app/` folder is where the agent lives and can be discovered by the Web UI.

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
