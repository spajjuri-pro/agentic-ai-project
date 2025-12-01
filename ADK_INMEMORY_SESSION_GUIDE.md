# ADK InMemorySessionService - Session Management Guide

## Overview

This guide explains how to replace custom session management with **ADK's built-in `InMemorySessionService`**. This is a cleaner, framework-integrated approach that follows ADK best practices.

---

## Why Use ADK's InMemorySessionService?

✅ **Built into ADK** — No custom SQLite management needed  
✅ **Session Lifecycle Management** — Create, resume, delete sessions seamlessly  
✅ **State Management** — `session.state` automatically handles data persistence  
✅ **Event Tracking** — All interactions automatically recorded  
✅ **Framework Integration** — Works with `Runner` and callbacks  
✅ **Less Code** — Remove all custom database logic  

---

## Core Concepts

### 1. SessionService
Manages the lifecycle of all sessions for your application.

```python
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
```

### 2. Session
Represents a single conversation thread with a user.

**Properties:**
- `id` — Unique session ID
- `app_name` — Application name (e.g., "my_agent_app")
- `user_id` — User identifier
- `state` — Key-value dictionary for storing conversation data
- `events` — Complete history of interactions
- `last_update_time` — Timestamp of last activity

### 3. Session State
A dictionary where you store data during the conversation.

```python
session.state["user:name"] = "John Smith"
session.state["user:age"] = 30
session.state["current_profile_id"] = 5
session.state["workout_plan"] = {...}
```

### 4. State Prefixes (Scopes)

| Prefix | Scope | Persistence | Example |
|--------|-------|-------------|---------|
| (none) | Session-specific | Lost on app restart | `session.state["current_step"]` |
| `user:` | User-wide | Persists across sessions | `session.state["user:name"]` |
| `app:` | App-wide | Shared by all users | `session.state["app:version"]` |
| `temp:` | Current invocation only | Discarded after response | `session.state["temp:validation_error"]` |

### 5. Runner
Orchestrates the agent execution within a session.

```python
from google.adk.runners import Runner

runner = Runner(
    agent=root_agent,
    app_name="my_agent_app",
    session_service=session_service
)
```

---

## Architecture with ADK Sessions

```
User Input
    ↓
Runner (with session_service)
    ↓
Session Created/Retrieved
    ↓
Agent Processes (reads session.state)
    ↓
Tool Execution (updates session.state)
    ↓
Event Created & Appended
    ↓
session.state Updated
    ↓
Response to User
```

---

## Implementation Steps

### Step 1: Initialize SessionService

```python
from google.adk.sessions import InMemorySessionService

# Create a global session service
session_service = InMemorySessionService()

# For development - simple and no external dependencies
# For production - consider DatabaseSessionService or VertexAiSessionService
```

### Step 2: Create or Resume Sessions

```python
# Create new session for a user
session = await session_service.create_session(
    app_name="my_agent_app",
    user_id="user123",
    state={
        "user:name": "John Smith",
        "user:age": 30
    }
)

# Resume existing session
sessions = await session_service.list_sessions(
    app_name="my_agent_app",
    user_id="user123"
)
existing_session = sessions[0]
```

### Step 3: Store Data in Session.State

Instead of custom `save_session()`, use `session.state`:

```python
# Store user profile in state
session.state["user:name"] = "John Smith"
session.state["user:profile_id"] = 5
session.state["current_workout_plan"] = workout_plan_dict
```

### Step 4: Access State in Tools

Your tool functions receive `ToolContext` with access to state:

```python
def my_tool(context: ToolContext) -> dict:
    # Read from state
    user_name = context.state.get("user:name")
    profile_id = context.state.get("user:profile_id")
    
    # Do work...
    result = {...}
    
    # Write to state
    context.state["temp:last_result"] = result
    
    return result
```

### Step 5: Use Runner for Agent Execution

```python
from google.adk.runners import Runner

runner = Runner(
    agent=root_agent,
    app_name="my_agent_app",
    session_service=session_service
)

# Run agent for a session
user_message = Content(parts=[Part(text="Create a workout plan for me")])

for event in runner.run(
    user_id="user123",
    session_id="session456",
    new_message=user_message
):
    if event.is_final_response():
        print(f"Agent: {event.content}")
```

---

## Working Example: Exercise Planner with ADK Sessions

### Before (Custom Session Management)

```python
# Manual SQLite management
def save_session(user_id, user_name, profile_data, workout_plan):
    conn = sqlite3.connect(SESSIONS_PATH)
    cursor = conn.cursor()
    # ... lots of SQL code ...
    return {"status": "success", "session_id": session_id}

def get_user_sessions(user_name):
    conn = sqlite3.connect(SESSIONS_PATH)
    # ... query and parse JSON ...
    return sessions_list
```

### After (ADK Session Management)

```python
# Simple state updates
session.state["user:name"] = name
session.state["user:profile"] = profile_dict
session.state["current_workout_plan"] = workout_plan_dict
session.state["refinement_history"] = []

# That's it! SessionService handles everything
```

---

## Tool Modifications

### Tool Function with Session State

```python
from google.adk.agents import tool
from google.adk.context import ToolContext

@tool(description="Save user profile")
def save_user_profile(
    context: ToolContext,
    name: str,
    age: int,
    height: str,
    weight: int,
    exercise_goal: str,
    injury: str = "None"
) -> dict:
    """Save profile and store in session state."""
    
    # Validate inputs
    if not name:
        return {"status": "error", "message": "Name cannot be empty"}
    
    # Create profile dict
    profile = {
        "name": name,
        "age": age,
        "height": height,
        "weight": weight,
        "exercise_goal": exercise_goal,
        "injury": injury
    }
    
    # Store in session state (persistent!)
    context.state["user:profile"] = profile
    context.state["user:name"] = name
    context.state["user:age"] = age
    
    return {
        "status": "success",
        "message": f"✅ Profile saved for {name}!"
    }

@tool(description="Get current user profile")
def get_user_profile(context: ToolContext) -> dict:
    """Retrieve profile from session state."""
    
    profile = context.state.get("user:profile")
    
    if profile:
        return {
            "status": "success",
            "profile": profile
        }
    else:
        return {
            "status": "error",
            "message": "No profile in this session"
        }

@tool(description="Add refinement request")
def add_refinement(
    context: ToolContext,
    refinement_type: str,
    details: str
) -> dict:
    """Log refinement to session history."""
    
    history = context.state.get("refinement_history", [])
    
    history.append({
        "type": refinement_type,
        "details": details,
        "timestamp": time.time()
    })
    
    context.state["refinement_history"] = history
    
    return {
        "status": "success",
        "refinement_count": len(history)
    }
```

---

## Session Lifecycle

### New User (First Time)

```python
# 1. Create session
session = await session_service.create_session(
    app_name="my_agent_app",
    user_id="alice"
)

# 2. User fills form, tools update state
# Tool: save_user_profile
context.state["user:name"] = "Alice"
context.state["user:profile"] = {...}

# 3. Generate workout plan
# Tool: generate_workout_plan
context.state["current_workout_plan"] = {...}

# 4. State automatically persisted when event appended
```

### Returning User (Pick Up Where Left Off)

```python
# 1. List sessions for user
sessions = await session_service.list_sessions(
    app_name="my_agent_app",
    user_id="alice"
)

# 2. Get most recent session
latest_session = sessions[0]  # Most recent first

# 3. Access previous data
profile = latest_session.state.get("user:profile")
workout_plan = latest_session.state.get("current_workout_plan")

# 4. Continue in same session
for event in runner.run(
    user_id="alice",
    session_id=latest_session.id,
    new_message=user_request
):
    # Agent can access and modify state
    pass
```

### Refinement Request

```python
# User: "Make the workout harder"

# In a tool or agent callback:
context.state["temp:refinement_requested"] = "increase_difficulty"

# Generate new plan
new_plan = generate_plan(context.state["user:profile"])
context.state["current_workout_plan"] = new_plan

# Log refinement
history = context.state.get("refinement_history", [])
history.append({"type": "difficulty_increase", "details": {...}})
context.state["refinement_history"] = history
```

---

## State Organization Best Practices

```python
# ✅ GOOD - Clear prefixes and structures
session.state["user:name"] = "John"
session.state["user:age"] = 30
session.state["user:preferences"] = {"theme": "dark"}
session.state["current_step"] = "collecting_profile"
session.state["workout_plan"] = {...}

# ❌ AVOID - No prefix or unclear naming
session.state["name"] = "John"
session.state["a"] = 30
session.state["data"] = {...}

# ✅ Use temp: for intermediate data
session.state["temp:validation_errors"] = [...] 
session.state["temp:api_response"] = {...}

# These are auto-discarded after invocation
```

---

## Comparison: Custom vs ADK Sessions

| Feature | Custom SQLite | ADK InMemory |
|---------|---------------|-------------|
| **Setup** | Manual SQLite schema | `InMemorySessionService()` |
| **Create Session** | SQL INSERT | `session_service.create_session()` |
| **Store Data** | `save_session()` function | `session.state["key"] = value` |
| **Retrieve Data** | `get_user_sessions()` function | `session.state.get("key")` |
| **Event Tracking** | Manual (we added it) | Built-in ✓ |
| **Refinements** | Custom `add_refinement_to_session()` | `session.state["refinement_history"]` |
| **Persistence** | SQLite files | In-memory (lost on restart) |
| **Code Complexity** | ~300 lines | ~50 lines |
| **Framework Integration** | External | Native ADK ✓ |

---

## Migration Path

### Phase 1: Parallel Implementation
- Keep existing custom session code
- Add ADK session initialization
- Run both side-by-side for testing

### Phase 2: Refactor Tools
- Update tools to use `ToolContext.state`
- Remove SQLite queries from tools
- Test with Runner

### Phase 3: Update Agent Instructions
- Modify agent prompt to reference session state
- Remove manual session management mentions
- Simplify workflow description

### Phase 4: Remove Custom Code
- Delete `sessions.db` related code
- Remove `save_session()`, `get_user_sessions()`, etc.
- Clean up imports

---

## Advanced: Persistent Sessions

For production, switch to `DatabaseSessionService`:

```python
from google.adk.sessions import DatabaseSessionService

# SQLite (local development)
db_url = "sqlite:///./adk_sessions.db"
session_service = DatabaseSessionService(db_url=db_url)

# PostgreSQL (production)
db_url = "postgresql://user:password@localhost/adk_sessions"
session_service = DatabaseSessionService(db_url=db_url)
```

Or use **VertexAiSessionService** for cloud-managed sessions:

```python
from google.adk.sessions import VertexAiSessionService

session_service = VertexAiSessionService(
    project="your-gcp-project",
    location="us-central1"
)
```

---

## Key ADK APIs

### InMemorySessionService

```python
# Create session
session = await service.create_session(
    app_name="app_name",
    user_id="user123",
    state={"initial": "state"}  # Optional
)

# List sessions for user
sessions = await service.list_sessions(app_name="app", user_id="user123")

# Get specific session
session = await service.get_session(app_name="app", user_id="user123", session_id="sess123")

# Delete session
await service.delete_session(app_name="app", user_id="user123", session_id="sess123")

# Append event (auto-updates state)
await service.append_event(session, event)
```

### Session Object

```python
# Read state
value = session.state["key"]
value = session.state.get("key", "default")

# View history
all_events = session.events

# Metadata
session.id
session.user_id
session.app_name
session.last_update_time
```

### ToolContext

```python
# In tool functions
def my_tool(context: ToolContext) -> dict:
    # Read state
    value = context.state.get("key")
    
    # Update state
    context.state["key"] = value
    
    # Access invocation ID for debugging
    invocation_id = context.invocation_id
    
    return result
```

---

## Troubleshooting

### Session State Not Persisting

**Problem:** State disappears after conversation ends.

**Cause:** `InMemorySessionService` doesn't persist to disk. Data is lost on app restart.

**Solution:** Use `DatabaseSessionService` for persistence.

```python
from google.adk.sessions import DatabaseSessionService
db_url = "sqlite:///./sessions.db"
session_service = DatabaseSessionService(db_url=db_url)
```

### State Key Missing in Instructions

**Problem:** Agent instruction references `{user:name}` but key doesn't exist.

**Solution:** Use optional key syntax `{user:name?}` or ensure key is set before agent runs.

```python
# In tool
context.state["user:name"] = name

# In agent instruction
instruction="User's name is {user:name}"  # Will be injected
```

### State Changes Not Reflected

**Problem:** Modified `session.state` directly but changes not saved.

**Cause:** Direct modification bypasses event tracking.

**Solution:** Always update state through `context.state` in tools/callbacks.

```python
# ❌ WRONG - retrieved session from service
retrieved_session = await service.get_session(...)
retrieved_session.state["key"] = value  # Not persisted!

# ✅ RIGHT - use context in tool
def my_tool(context: ToolContext):
    context.state["key"] = value  # Properly tracked
```

---

## Summary

| Aspect | ADK Approach |
|--------|-------------|
| **Core** | `InMemorySessionService` creates/manages sessions |
| **Storage** | `session.state` dictionary (key-value pairs) |
| **Tools** | Receive `ToolContext`, access `context.state` |
| **Execution** | `Runner` orchestrates with `session_service` |
| **Events** | Auto-created, state updates tracked |
| **Persistence** | In-memory (temp), or use `DatabaseSessionService` (permanent) |
| **Framework** | Native ADK integration, no custom code |

**Result:** Clean, maintainable, framework-integrated session management! ✨

