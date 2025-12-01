# Web UI Usage Guide

**📖 For End Users & Developers** — How to use the Exercise Planner through the Web UI.

## Starting the Web Server

```bash
cd /Users/spajjuri/my_agent
source .venv/bin/activate
adk web --port 8000
```

Then open: **http://localhost:8000**

The agent will automatically be discovered and displayed as "my_agent_app" in the Web UI.

## How the Agent Works

The agent has **4 tools** available:

1. **collect_user_profile_form** - Displays the form structure
2. **save_user_profile** - Saves profile to database with validation
3. **get_latest_user_profile** - Retrieves saved profile from database
4. **generate_weekly_workout_plan_from_profile** - Creates personalized workout plan

## Expected User Interaction Flow

### Step 1: Start Conversation
```
You: Hi, I want a personalized workout plan
```

### Step 2: Agent Shows Form Structure
The agent will display information about the form fields it needs:
- Full Name
- Age
- Height
- Weight
- Fitness Goal
- Injuries/Limitations

### Step 3: Provide Your Information
Respond with your profile information. The agent will ask for each field:

```
You: My name is John Smith, I'm 35 years old, 5'10", 180 lbs, 
I want to do Weight Loss training, and I have no injuries.
```

Or you can provide it piece by piece as the agent asks.

### Step 4: Profile Saved
Agent confirms: 
```
✅ Profile Saved Successfully!
Profile ID: 1
Name: John Smith
Age: 35 years
Height: 5'10"
Weight: 180 lbs
Goal: Weight Loss
Injuries: None

Now generating your personalized workout plan...
```

### Step 5: Workout Plan Generated
Agent presents your personalized weekly schedule:
```
Monday: Cardio & Abdominals
- Exercise 1: ...
- Exercise 2: ...

Tuesday: Legs & Glutes
- Exercise 1: ...
- Exercise 2: ...

[etc...]
```

## Troubleshooting

### If form is not showing up:

1. **Clear cache and restart server:**
   ```bash
   cd /Users/spajjuri/my_agent
   find . -type d -name __pycache__ -exec rm -rf {} +
   find . -type f -name "*.pyc" -delete
   
   # Restart web server
   pkill -f "adk web"
   sleep 2
   /Users/spajjuri/my_agent/.venv/bin/adk web --port 8000
   ```

2. **Verify tools are loaded:**
   ```bash
   cd /Users/spajjuri/my_agent
   python3 -c "from my_agent_app import root_agent; print(f'Tools: {[t.__name__ for t in root_agent.tools]}')"
   ```
   
   Should output:
   ```
   Tools: ['collect_user_profile_form', 'save_user_profile', 'get_latest_user_profile', 'generate_weekly_workout_plan_from_profile']
   ```

3. **Refresh browser:** Hard refresh (Cmd+Shift+R on macOS)

## Direct Tool Testing

You can also test the form directly without the Web UI:

```python
from my_agent_app import root_agent
import json

# Get the collect_user_profile_form tool
form_tool = [t for t in root_agent.tools if hasattr(t, '__name__') and t.__name__ == 'collect_user_profile_form'][0]
form = form_tool()
print(json.dumps(form, indent=2))
```

This will output the complete form structure with all fields, validation rules, placeholders, etc.

## Notes

- The `collect_user_profile_form()` tool provides **form metadata/structure**
- The agent uses this to guide the conversation
- Each field has:
  - Type (text, number, select)
  - Validation rules (min/max)
  - Placeholder text
  - Description
  - Required flag

- The form is **not a rendered HTML form** but a structured data response that guides the LLM agent to ask questions in sequence

## Example Complete Interaction

```
You: Create a workout plan for me

Agent: I'd be happy to help you create a personalized workout plan! 
I need to collect some information about you first.

Here's what I'll ask for:
📋 User Profile Registration

Please provide:
1. Full Name - Enter your first and last name
2. Age - Enter your age in years (13-120)
3. Height - Enter your height (e.g., 5'10", 180 cm)
4. Weight - Enter your weight in pounds (50-500 lbs)
5. Fitness Goal - Choose: Weight Loss, Strength Building, or Cardio
6. Injuries/Limitations - Any injuries (optional)

Let's start! What is your full name?

You: Jane Smith

Agent: Great to meet you, Jane Smith! 
Next, how old are you?

You: 28

Agent: Perfect! At 28 years old, I can tailor your plan for active adults.
What's your height? (e.g., 5'8", 170 cm)

You: 5'8"

Agent: Excellent! Now, what's your current weight in pounds?

You: 140

Agent: Got it! 5'8" and 140 lbs - noted.
What's your primary fitness goal? 
Choose from: Weight Loss, Strength Building, or Cardio

You: Weight Loss

Agent: Weight Loss - a great goal! That means we'll focus on cardio and high-rep exercises.
Do you have any injuries or physical limitations? (Just type "None" if you don't)

You: None

Agent: ✅ Profile Saved Successfully!

Profile ID: 1
Name: Jane Smith
Age: 28 years
Height: 5'8"
Weight: 140 lbs
Goal: Weight Loss
Injuries: None

Now generating your personalized workout plan...

📋 Your Personalized Weekly Workout Plan

Goal: Weight Loss | Difficulty: Intermediate | Frequency: 5-6 days per week

Monday - Cardio & Abdominals
- Burpees (30 reps)
- Mountain Climbers (40 reps)
- Jumping Jacks (50 reps)

[... continues through Sunday ...]
```
