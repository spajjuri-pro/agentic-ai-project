# Setup Guide

Complete setup instructions for the ADK Agent project.

## Prerequisites

- Python 3.9+
- Google Cloud account with 300 free credits
- gcloud CLI installed and configured
- Git

## Setup Steps

### 1. Clone the repo

```bash
git clone https://github.com/spajjuri-pro/agentic-ai-project.git
cd agentic-ai-project
```

### 2. Create a virtual environment

```bash
cd my_agent
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install google-ai-generativelanguage google-cloud-aiplatform google-adk
```

### 4. Set up credentials (Vertex AI requires service account, not API key)

**Why service account?** Vertex AI API requires OAuth2 authentication; API keys are not supported.

#### Create a service account

```bash
export PROJECT_ID="YOUR_GCP_PROJECT_ID"
gcloud config set project $PROJECT_ID

# Create service account
gcloud iam service-accounts create adk-agent-sa --display-name="ADK agent"

# Grant Vertex AI User role
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:adk-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Create and download JSON key
gcloud iam service-accounts keys create ~/adk-agent-sa-key.json \
  --iam-account="adk-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com"
```

#### Configure `.env`

```bash
cp .env.example .env
```

Edit `.env`:

```properties
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_APPLICATION_CREDENTIALS=~/adk-agent-sa-key.json
```

⚠️ **Security**: Never commit `.env` or the service account JSON file. They are in `.gitignore`.

### 5. Enable required APIs

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativelanguage.googleapis.com
```

## Troubleshooting

### 401 UNAUTHENTICATED

**Error**: `API keys are not supported by this API. Expected OAuth2 access token...`

**Fix**: You're using an API key with Vertex AI. Use a service account (steps 4) instead.

### 429 RESOURCE_EXHAUSTED

**Error**: `You exceeded your current quota...`

**Possible causes**:
- Free tier quota exhausted for the model
- Billing not enabled

**Fix**:
1. Check GCP Billing console: enable billing if needed
2. Check [ai.dev/usage](https://ai.dev/usage?tab=rate-limit) for current quota usage
3. Switch to a different model with available quota
4. Request quota increase from [Cloud Console Quotas](https://console.cloud.google.com/iam-admin/quotas)

### Missing APIs

**Error**: `The Compute API has not been used in project...`

**Fix**: Enable the required APIs:

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativelanguage.googleapis.com
gcloud services enable compute.googleapis.com
```

## File structure

```
my_agent/
├── my_agent_app/           ← Agent package (ADK discovery point)
│   ├── __init__.py         ← Exports root_agent
│   ├── agent.py            ← Main agent definition
│   ├── megaGymDataset.csv  ← Exercise database
│   └── user_profiles.db    ← SQLite database for user profiles
├── __init__.py             ← Root package exports
├── .env                    ← Local credentials (NOT committed)
├── .env.example            ← Template for environment variables
├── README.md               ← Quick start guide
└── README-SETUP.md         ← This detailed setup guide
```

**Key Change**: Agent is now in `my_agent_app/` subdirectory because ADK discovers agents by looking for package directories (folders with `__init__.py`), not individual files.

## Next steps

1. Complete setup steps above
2. Make sure you're in `/Users/spajjuri/my_agent` directory
3. See [README.md](./README.md) for quick start commands
4. Run `adk web --port 8000` to launch the web UI (agent will be auto-discovered)
5. Run `adk run my_agent.my_agent_app` to execute the agent from CLI

## More info

- [ADK docs](https://google.github.io/adk-docs/)
- [Vertex AI docs](https://cloud.google.com/vertex-ai/docs)
- [gcloud CLI reference](https://cloud.google.com/sdk/gcloud)
