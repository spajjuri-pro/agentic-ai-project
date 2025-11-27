# My Agent — Google ADK Demo

A demo agent using Google's ADK (Agent Development Kit) with Vertex AI.

## Setup

### Prerequisites
- Python 3.9+
- Google Cloud account with 300 free credits
- gcloud CLI installed and configured

### 1. Clone the repo
```bash
git clone https://github.com/spajjuri-pro/agentic-ai-project.git
cd agentic-ai-project
```

### 2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install google-ai-generativelanguage google-cloud-aiplatform google-adk
```

### 4. Set up credentials (Vertex AI requires service account, not API key)

**Create a service account:**
```bash
export PROJECT_ID="YOUR_GCP_PROJECT_ID"
gcloud config set project $PROJECT_ID
gcloud iam service-accounts create adk-agent-sa --display-name="ADK agent"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:adk-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
gcloud iam service-accounts keys create ~/adk-agent-sa-key.json \
  --iam-account="adk-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com"
```

**Configure `.env`:**
Copy `.env.example` to `.env` and update:
```bash
cp .env.example .env
```

Edit `.env`:
```properties
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_APPLICATION_CREDENTIALS=~/adk-agent-sa-key.json
```

## Quick Start

### Activate venv and run
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

## Troubleshooting

- **401 UNAUTHENTICATED**: You're using an API key with Vertex AI. Use a service account instead (see step 4 above).
- **429 RESOURCE_EXHAUSTED**: Your quota is exhausted or you don't have billing enabled. Check your GCP Billing console and enable if needed.

## File structure
- `agent.py` — Main agent definition
- `.env.example` — Template for environment variables (commit this, not `.env`)
- `.env` — Local credentials (do NOT commit)

## More info
- [ADK docs](https://google.github.io/adk-docs/)
- [Vertex AI docs](https://cloud.google.com/vertex-ai/docs)
