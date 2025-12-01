"""ADK Exercise Planner with InMemorySessionService - Refactored for ADK Sessions."""

import csv
import os
from google.adk.agents import LlmAgent, tool
from google.adk.context import ToolContext


DATASET_PATH = os.path.join(os.path.dirname(__file__), "megaGymDataset.csv")


def load_gym_dataset() -> list:
    """Load exercises from the CSV dataset."""
    exercises = []
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                exercises.append(row)
    except FileNotFoundError:
        return []
    return exercises


def get_exercises_by_goal_and_body_part(
    goal: str, body_parts: list, difficulty: str = "Intermediate"
) -> dict:
    """Filters exercises from the dataset based on goal and body parts."""
    exercises = load_gym_dataset()
    filtered = {}
    goal_type_map = {
        "Weight Loss": ["Cardio", "Plyometrics"],
        "Strength Building": ["Strength"],
        "Cardio": ["Cardio", "Plyometrics"],
    }
    exercise_types = goal_type_map.get(goal, ["Strength"])
    for body_part in body_parts:
        matching = [
            ex
            for ex in exercises
            if ex.get("Type") in exercise_types
            and ex.get("BodyPart") == body_part
            and ex.get("Level") == difficulty
            and ex.get("Title")
        ]
        if matching:
            filtered[body_part] = [
                {
                    "title": ex.get("Title", "Unknown"),
                    "description": ex.get("Desc", "No description"),
                    "equipment": ex.get("Equipment", "Bodyweight"),
                    "rating": ex.get("Rating", "N/A"),
                }
                for ex in matching[:5]
            ]
    return filtered


@tool(description="Display interactive user profile form")
def collect_user_profile_form(context: ToolContext) -> dict:
    """Interactive form to collect user profile details.
    
    Stores form structure in temp state for agent to display.
    """
    form_structure = {
        "status": "form_ready",
        "form_title": "📋 User Profile Registration",
        "fields": [
            {
                "field_name": "name",
                "label": "Full Name",
                "placeholder": "e.g., John Smith",
                "type": "text",
                "required": True,
                "description": "Enter your first and last name"
            },
            {
                "field_name": "age",
                "label": "Age",
                "placeholder": "e.g., 30",
                "type": "number",
                "min": 13,
                "max": 120,
                "required": True,
                "description": "Enter your age in years"
            },
            {
                "field_name": "height",
                "label": "Height",
                "placeholder": "e.g., 5'10\" or 180 cm",
                "type": "text",
                "required": True,
                "description": "Enter your height (e.g., 5'10\", 6'2\", 180 cm)"
            },
            {
                "field_name": "weight",
                "label": "Weight",
                "placeholder": "e.g., 180",
                "type": "number",
                "min": 50,
                "max": 500,
                "required": True,
                "description": "Enter your weight in pounds"
            },
            {
                "field_name": "exercise_goal",
                "label": "Fitness Goal",
                "type": "select",
                "required": True,
                "description": "What is your primary fitness goal?",
                "options": ["Weight Loss", "Strength Building", "Cardio"]
            },
            {
                "field_name": "injury",
                "label": "Injuries or Limitations",
                "placeholder": "e.g., None, Knee pain, Back strain",
                "type": "text",
                "required": False,
                "description": "Any current injuries or physical limitations?"
            }
        ],
        "message": "Please fill out your profile. This helps create a personalized plan!"
    }
    
    # Store form in temporary state for this invocation
    context.state["temp:form_structure"] = form_structure
    
    return form_structure


@tool(description="Save user profile to session state")
def save_user_profile(
    context: ToolContext,
    name: str,
    age: int,
    height: str,
    weight: int,
    exercise_goal: str,
    injury: str = "None"
) -> dict:
    """Save user profile to session state with validation.
    
    Stores profile in both user-scoped and session-scoped state for easy access.
    """
    try:
        # Validate inputs
        if not name or name.strip() == "":
            return {"status": "error", "message": "Name cannot be empty"}
        if age < 13 or age > 120:
            return {"status": "error", "message": "Age must be between 13 and 120"}
        if not height or height.strip() == "":
            return {"status": "error", "message": "Height cannot be empty"}
        if weight < 50 or weight > 500:
            return {"status": "error", "message": "Weight must be between 50 and 500 lbs"}
        if exercise_goal not in ["Weight Loss", "Strength Building", "Cardio"]:
            return {"status": "error", "message": "Invalid exercise goal"}
        
        # Use "None" if injury is empty
        if not injury or injury.lower().strip() in ["", "none", "n/a"]:
            injury = "None"
        
        # Create profile dictionary
        profile = {
            "name": name.strip(),
            "age": age,
            "height": height.strip(),
            "weight": weight,
            "exercise_goal": exercise_goal,
            "injury": injury,
        }
        
        # Store in session state - user-scoped for persistence across sessions
        context.state["user:name"] = name.strip()
        context.state["user:age"] = age
        context.state["user:height"] = height.strip()
        context.state["user:weight"] = weight
        context.state["user:exercise_goal"] = exercise_goal
        context.state["user:injury"] = injury
        
        # Also store complete profile for this session
        context.state["current_profile"] = profile
        
        return {
            "status": "success",
            "message": (
                f"✅ Profile Saved Successfully!\n\n"
                f"**Name:** {name.strip()}\n"
                f"**Age:** {age} years\n"
                f"**Height:** {height.strip()}\n"
                f"**Weight:** {weight} lbs\n"
                f"**Goal:** {exercise_goal}\n"
                f"**Injuries:** {injury}\n\n"
                f"Now generating your personalized workout plan..."
            ),
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save profile: {str(e)}"}


@tool(description="Get current user profile from session")
def get_user_profile(context: ToolContext) -> dict:
    """Retrieve user profile from session state."""
    try:
        profile = context.state.get("current_profile")
        
        if profile:
            return {
                "status": "success",
                "profile": profile,
            }
        else:
            return {
                "status": "error",
                "message": "No user profile in current session. Please create one first.",
            }
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve profile: {str(e)}"}


@tool(description="Generate personalized weekly workout plan")
def generate_weekly_workout_plan(context: ToolContext) -> dict:
    """Generate weekly workout plan based on profile in session state."""
    try:
        profile = context.state.get("current_profile")
        
        if not profile:
            return {
                "status": "error",
                "message": "No profile found. Please create a profile first."
            }
        
        goal = profile.get("exercise_goal", "Strength Building")
        user_age = profile.get("age", 30)
        injury = profile.get("injury", "None")
        weight = profile.get("weight", 170)
        
        # Determine body parts by goal
        goal_body_parts = {
            "Weight Loss": ["Abdominals", "Legs", "Back", "Chest"],
            "Strength Building": ["Back", "Chest", "Legs", "Abdominals"],
            "Cardio": ["Abdominals", "Legs", "Cardiovascular"],
        }
        body_parts = goal_body_parts.get(goal, ["Abdominals", "Chest", "Back"])
        
        # Determine difficulty
        difficulty = "Intermediate"
        if user_age < 18 or weight > 250 or user_age > 60:
            difficulty = "Beginner"
        
        # Get exercises
        exercises_by_part = get_exercises_by_goal_and_body_part(goal, body_parts, difficulty)
        
        # Build weekly plan
        weekly_plan = {
            "user_name": profile.get("name"),
            "goal": goal,
            "difficulty": difficulty,
            "frequency": {
                "Weight Loss": "5-6 days per week",
                "Strength Building": "4-5 days per week",
                "Cardio": "4-6 days per week",
            }.get(goal, "4-5 days per week"),
            "weekly_schedule": {
                "Monday": {
                    "focus": list(exercises_by_part.keys())[0] if exercises_by_part else "Rest",
                    "exercises": list(exercises_by_part.values())[0] if exercises_by_part else [],
                },
                "Tuesday": {
                    "focus": list(exercises_by_part.keys())[1] if len(exercises_by_part) > 1 else "Rest",
                    "exercises": list(exercises_by_part.values())[1] if len(exercises_by_part) > 1 else [],
                },
                "Wednesday": {"focus": "Rest or Light Cardio", "exercises": []},
                "Thursday": {
                    "focus": list(exercises_by_part.keys())[2] if len(exercises_by_part) > 2 else "Rest",
                    "exercises": list(exercises_by_part.values())[2] if len(exercises_by_part) > 2 else [],
                },
                "Friday": {
                    "focus": list(exercises_by_part.keys())[3] if len(exercises_by_part) > 3 else "Rest",
                    "exercises": list(exercises_by_part.values())[3] if len(exercises_by_part) > 3 else [],
                },
                "Saturday": {"focus": "Active Recovery or Light Stretching", "exercises": []},
                "Sunday": {"focus": "Rest Day", "exercises": []},
            },
        }
        
        if injury and injury.lower() != "none":
            weekly_plan["injury_modifications"] = (
                f"⚠️  Important: {profile.get('name')}, you have '{injury}'. "
                "Please avoid high-impact exercises and consult a physical therapist. "
                "Low-impact alternatives recommended."
            )
        
        # Store plan in session state
        context.state["current_workout_plan"] = weekly_plan
        
        # Initialize refinement history if not present
        if "refinement_history" not in context.state:
            context.state["refinement_history"] = []
        
        return {
            "status": "success",
            "workout_plan": weekly_plan,
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to generate plan: {str(e)}"}


@tool(description="Log refinement request to history")
def log_refinement_request(
    context: ToolContext,
    refinement_type: str,
    details: str
) -> dict:
    """Log a refinement request to the session's refinement history.
    
    Refinement types: difficulty_increase, difficulty_decrease, goal_change,
    focus_change, injury_update, custom
    """
    try:
        # Get existing history
        history = context.state.get("refinement_history", [])
        
        # Add new refinement
        refinement = {
            "type": refinement_type,
            "details": details,
        }
        history.append(refinement)
        
        # Update state
        context.state["refinement_history"] = history
        
        return {
            "status": "success",
            "message": f"✅ Refinement logged: {refinement_type}",
            "refinement_count": len(history)
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to log refinement: {str(e)}"}


# Define the root agent
root_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    name="root_agent",
    description="Exercise Planner with ADK Session Management - Personalizes workouts based on user profile and stores sessions.",
    instruction=(
        "You are an Exercise Planner Assistant using ADK Session Management.\n\n"
        "**YOUR WORKFLOW:**\n\n"
        "**STEP 1: GREET & CHECK SESSION**\n"
        "- Greet the user warmly\n"
        "- Note: The Runner has created a session for this user\n"
        "- Check if user:name exists in session state to see if they're returning\n"
        "- If returning: 'Welcome back, {user:name?}! I see you have a previous plan. Would you like to refine it or create a new one?'\n"
        "- If new: 'Welcome! Let's create your personalized workout plan.'\n\n"
        "**STEP 2: COLLECT PROFILE (New Users)**\n"
        "- Call collect_user_profile_form to display the form\n"
        "- Collect responses for each field:\n"
        "  • Name, Age, Height, Weight, Fitness Goal, Injuries\n"
        "- Present each field clearly, one at a time\n\n"
        "**STEP 3: SAVE PROFILE**\n"
        "- Call save_user_profile with all collected data\n"
        "- This stores in session state automatically\n"
        "- Confirm save and show summary\n\n"
        "**STEP 4: GENERATE PLAN**\n"
        "- Call get_user_profile to verify data is in session\n"
        "- Call generate_weekly_workout_plan\n"
        "- This creates plan based on profile and stores in session.state\n"
        "- Present the weekly schedule with exercises for each day\n\n"
        "**STEP 5: REFINEMENT HANDLING**\n"
        "If user wants to refine:\n"
        "- Ask what to change (difficulty, goal, focus area, etc.)\n"
        "- Update profile: call save_user_profile with changes\n"
        "- Generate new plan: call generate_weekly_workout_plan\n"
        "- Log refinement: call log_refinement_request\n"
        "- Show refined plan\n\n"
        "**STEP 6: PROVIDE GUIDANCE**\n"
        "- Recommend workout frequency based on goal\n"
        "- Share safety tips and form guidance\n"
        "- Remind about consulting doctor for serious injuries\n"
        "- Suggest rest and recovery strategies\n\n"
        "**IMPORTANT NOTES:**\n"
        "- All data persists in session.state during this conversation\n"
        "- User-scoped data (user:name, user:age, etc.) persists across sessions\n"
        "- Be friendly, encouraging, and supportive\n"
        "- Reference session state values naturally in conversation\n"
        "- Always validate inputs before saving\n"
    ),
    tools=[
        collect_user_profile_form,
        save_user_profile,
        get_user_profile,
        generate_weekly_workout_plan,
        log_refinement_request,
    ],
)

