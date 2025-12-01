"""ADK Exercise Planner Agent - Generates personalized workout plans.""""""ADK Sequential Agents - Exercise Planner with User Profile Database & Session Management."""



import csvimport csv

import osimport json

from google.adk.agents.llm_agent import Agentimport os

import sqlite3

from datetime import datetime

DATASET_PATH = os.path.join(os.path.dirname(__file__), "megaGymDataset.csv")from google.adk.agents.llm_agent import Agent





def collect_user_profile_form() -> dict:DATASET_PATH = os.path.join(os.path.dirname(__file__), "megaGymDataset.csv")

    """Interactive form to collect user profile details one field at a time.DB_PATH = os.path.join(os.path.dirname(__file__), "user_profiles.db")

    SESSIONS_PATH = os.path.join(os.path.dirname(__file__), "sessions.db")

    Returns a formatted form structure that the agent can use to collect input

    from the user field by field.

    """def init_database():

    return {    """Initialize SQLite database with user profiles table."""

        "status": "form_ready",    conn = sqlite3.connect(DB_PATH)

        "form_title": "📋 User Profile Registration",    cursor = conn.cursor()

        "fields": [    cursor.execute(

            {        """

                "field_name": "name",        CREATE TABLE IF NOT EXISTS user_profiles (

                "label": "Full Name",            id INTEGER PRIMARY KEY AUTOINCREMENT,

                "placeholder": "e.g., John Smith",            name TEXT NOT NULL,

                "type": "text",            age INTEGER NOT NULL,

                "required": True,            height TEXT NOT NULL,

                "description": "Enter your first and last name"            weight INTEGER NOT NULL,

            },            exercise_goal TEXT NOT NULL,

            {            injury TEXT DEFAULT 'None',

                "field_name": "age",            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                "label": "Age",        )

                "placeholder": "e.g., 30",        """

                "type": "number",    )

                "min": 13,    conn.commit()

                "max": 120,    conn.close()

                "required": True,

                "description": "Enter your age in years"

            },def init_sessions_database():

            {    """Initialize SQLite database for session management."""

                "field_name": "height",    conn = sqlite3.connect(SESSIONS_PATH)

                "label": "Height",    cursor = conn.cursor()

                "placeholder": "e.g., 5'10\" or 180 cm",    cursor.execute(

                "type": "text",        """

                "required": True,        CREATE TABLE IF NOT EXISTS sessions (

                "description": "Enter your height (e.g., 5'10\", 6'2\", 180 cm, 170 cm)"            session_id INTEGER PRIMARY KEY AUTOINCREMENT,

            },            user_id INTEGER NOT NULL,

            {            user_name TEXT NOT NULL,

                "field_name": "weight",            profile_data JSON NOT NULL,

                "label": "Weight",            workout_plan JSON NOT NULL,

                "placeholder": "e.g., 180",            refinement_history JSON DEFAULT '[]',

                "type": "number",            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                "min": 50,            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                "max": 500,            FOREIGN KEY (user_id) REFERENCES user_profiles(id)

                "required": True,        )

                "description": "Enter your weight in pounds"        """

            },    )

            {    conn.commit()

                "field_name": "exercise_goal",    conn.close()

                "label": "Fitness Goal",

                "type": "select",

                "required": True,def collect_user_profile_form() -> dict:

                "description": "What is your primary fitness goal?",    """Interactive form to collect user profile details one field at a time.

                "options": ["Weight Loss", "Strength Building", "Cardio"]    

            },    Returns a formatted form structure that the agent can use to collect input

            {    from the user field by field.

                "field_name": "injury",    """

                "label": "Injuries or Limitations",    return {

                "placeholder": "e.g., None, Knee pain, Back strain",        "status": "form_ready",

                "type": "text",        "form_title": "📋 User Profile Registration",

                "required": False,        "fields": [

                "description": "Any current injuries or physical limitations? (Leave empty for None)"            {

            }                "field_name": "name",

        ],                "label": "Full Name",

        "message": "Please fill out your profile information below. This helps us create a personalized workout plan just for you!"                "placeholder": "e.g., John Smith",

    }                "type": "text",

                "required": True,

                "description": "Enter your first and last name"

def validate_user_profile(            },

    name: str, age: int, height: str, weight: int, exercise_goal: str, injury: str = "None"            {

) -> dict:                "field_name": "age",

    """Validate user profile inputs.                "label": "Age",

                    "placeholder": "e.g., 30",

    Args:                "type": "number",

        name: User's full name.                "min": 13,

        age: User's age in years.                "max": 120,

        height: User's height (e.g., "5'10\"", "180 cm").                "required": True,

        weight: User's weight in pounds.                "description": "Enter your age in years"

        exercise_goal: Exercise goal ("Weight Loss", "Strength Building", or "Cardio").            },

        injury: Any injuries or limitations (default: "None").            {

                        "field_name": "height",

    Returns:                "label": "Height",

        A dictionary with validation status and the profile data.                "placeholder": "e.g., 5'10\" or 180 cm",

    """                "type": "text",

    try:                "required": True,

        # Validate inputs                "description": "Enter your height (e.g., 5'10\", 6'2\", 180 cm, 170 cm)"

        if not name or name.strip() == "":            },

            return {"status": "error", "message": "Name cannot be empty"}            {

        if age < 13 or age > 120:                "field_name": "weight",

            return {"status": "error", "message": "Age must be between 13 and 120"}                "label": "Weight",

        if not height or height.strip() == "":                "placeholder": "e.g., 180",

            return {"status": "error", "message": "Height cannot be empty"}                "type": "number",

        if weight < 50 or weight > 500:                "min": 50,

            return {"status": "error", "message": "Weight must be between 50 and 500 lbs"}                "max": 500,

        if exercise_goal not in ["Weight Loss", "Strength Building", "Cardio"]:                "required": True,

            return {"status": "error", "message": "Invalid exercise goal"}                "description": "Enter your weight in pounds"

                    },

        # Use "None" if injury is empty            {

        if not injury or injury.lower().strip() in ["", "none", "n/a"]:                "field_name": "exercise_goal",

            injury = "None"                "label": "Fitness Goal",

                        "type": "select",

        return {                "required": True,

            "status": "success",                "description": "What is your primary fitness goal?",

            "profile": {                "options": ["Weight Loss", "Strength Building", "Cardio"]

                "name": name.strip(),            },

                "age": age,            {

                "height": height.strip(),                "field_name": "injury",

                "weight": weight,                "label": "Injuries or Limitations",

                "exercise_goal": exercise_goal,                "placeholder": "e.g., None, Knee pain, Back strain",

                "injury": injury.strip(),                "type": "text",

                "message": (                "required": False,

                    f"✅ Profile validated successfully!\n\n"                "description": "Any current injuries or physical limitations? (Leave empty for None)"

                    f"**Name:** {name.strip()}\n"            }

                    f"**Age:** {age} years\n"        ],

                    f"**Height:** {height.strip()}\n"        "message": "Please fill out your profile information below. This helps us create a personalized workout plan just for you!"

                    f"**Weight:** {weight} lbs\n"    }

                    f"**Goal:** {exercise_goal}\n"

                    f"**Injuries:** {injury.strip()}\n\n"

                    f"Now generating your personalized workout plan..."def save_user_profile(

                ),    name: str, age: int, height: str, weight: int, exercise_goal: str, injury: str = "None"

            },) -> dict:

        }    """Save user profile to SQLite database.

    except Exception as e:    

        return {"status": "error", "message": f"Failed to validate profile: {str(e)}"}    Args:

        name: User's full name.

        age: User's age in years.

def load_gym_dataset() -> list:        height: User's height (e.g., "5'10\"", "180 cm").

    """Load exercises from the CSV dataset."""        weight: User's weight in pounds.

    exercises = []        exercise_goal: Exercise goal ("Weight Loss", "Strength Building", or "Cardio").

    try:        injury: Any injuries or limitations (default: "None").

        with open(DATASET_PATH, "r", encoding="utf-8") as f:        

            reader = csv.DictReader(f)    Returns:

            for row in reader:        A dictionary with save status and user profile ID.

                exercises.append(row)    """

    except FileNotFoundError:    try:

        return []        init_database()

    return exercises        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        

def get_exercises_by_goal_and_body_part(        # Validate inputs

    goal: str, body_parts: list, difficulty: str = "Intermediate"        if not name or name.strip() == "":

) -> dict:            return {"status": "error", "message": "Name cannot be empty"}

    """Filters exercises from the dataset based on goal and body parts."""        if age < 13 or age > 120:

    exercises = load_gym_dataset()            return {"status": "error", "message": "Age must be between 13 and 120"}

    filtered = {}        if not height or height.strip() == "":

    goal_type_map = {            return {"status": "error", "message": "Height cannot be empty"}

        "Weight Loss": ["Cardio", "Plyometrics"],        if weight < 50 or weight > 500:

        "Strength Building": ["Strength"],            return {"status": "error", "message": "Weight must be between 50 and 500 lbs"}

        "Cardio": ["Cardio", "Plyometrics"],        if exercise_goal not in ["Weight Loss", "Strength Building", "Cardio"]:

    }            return {"status": "error", "message": "Invalid exercise goal"}

    exercise_types = goal_type_map.get(goal, ["Strength"])        

    for body_part in body_parts:        # Use "None" if injury is empty

        matching = [        if not injury or injury.lower().strip() in ["", "none", "n/a"]:

            ex            injury = "None"

            for ex in exercises        

            if ex.get("Type") in exercise_types        cursor.execute(

            and ex.get("BodyPart") == body_part            """

            and ex.get("Level") == difficulty            INSERT INTO user_profiles (name, age, height, weight, exercise_goal, injury)

            and ex.get("Title")            VALUES (?, ?, ?, ?, ?, ?)

        ]            """,

        if matching:            (name.strip(), age, height.strip(), weight, exercise_goal, injury.strip()),

            filtered[body_part] = [        )

                {        conn.commit()

                    "title": ex.get("Title", "Unknown"),        profile_id = cursor.lastrowid

                    "description": ex.get("Desc", "No description"),        conn.close()

                    "equipment": ex.get("Equipment", "Bodyweight"),        

                    "rating": ex.get("Rating", "N/A"),        return {

                }            "status": "success",

                for ex in matching[:5]            "profile_id": profile_id,

            ]            "name": name.strip(),

    return filtered            "age": age,

            "height": height.strip(),

            "weight": weight,

def generate_weekly_workout_plan(profile: dict) -> dict:            "exercise_goal": exercise_goal,

    """Generates a weekly workout plan based on user profile."""            "injury": injury,

    goal = profile.get("exercise_goal", "Strength Building")            "message": (

    user_age = profile.get("age", 30)                f"✅ Profile Saved Successfully!\n\n"

    injury = profile.get("injury", "None")                f"**Profile ID:** {profile_id}\n"

    weight = profile.get("weight", 170)                f"**Name:** {name.strip()}\n"

                    f"**Age:** {age} years\n"

    goal_body_parts = {                f"**Height:** {height.strip()}\n"

        "Weight Loss": ["Abdominals", "Legs", "Back", "Chest"],                f"**Weight:** {weight} lbs\n"

        "Strength Building": ["Back", "Chest", "Legs", "Abdominals"],                f"**Goal:** {exercise_goal}\n"

        "Cardio": ["Abdominals", "Legs", "Cardiovascular"],                f"**Injuries:** {injury}\n\n"

    }                f"Now generating your personalized workout plan..."

    body_parts = goal_body_parts.get(goal, ["Abdominals", "Chest", "Back"])            ),

            }

    difficulty = "Intermediate"    except Exception as e:

    if user_age < 18 or weight > 250 or user_age > 60:        return {"status": "error", "message": f"Failed to save profile: {str(e)}"}

        difficulty = "Beginner"

    

    exercises_by_part = get_exercises_by_goal_and_body_part(goal, body_parts, difficulty)def get_latest_user_profile() -> dict:

        """Retrieve the most recently created user profile from the database."""

    weekly_plan = {    try:

        "user_name": profile.get("name"),        init_database()

        "goal": goal,        conn = sqlite3.connect(DB_PATH)

        "difficulty": difficulty,        cursor = conn.cursor()

        "frequency": {        cursor.execute(

            "Weight Loss": "5-6 days per week",            """

            "Strength Building": "4-5 days per week",            SELECT id, name, age, height, weight, exercise_goal, injury

            "Cardio": "4-6 days per week",            FROM user_profiles

        }.get(goal, "4-5 days per week"),            ORDER BY created_at DESC

        "weekly_schedule": {            LIMIT 1

            "Monday": {            """

                "focus": list(exercises_by_part.keys())[0] if exercises_by_part else "Rest",        )

                "exercises": list(exercises_by_part.values())[0] if exercises_by_part else [],        row = cursor.fetchone()

            },        conn.close()

            "Tuesday": {        if row:

                "focus": list(exercises_by_part.keys())[1] if len(exercises_by_part) > 1 else "Rest",            return {

                "exercises": list(exercises_by_part.values())[1] if len(exercises_by_part) > 1 else [],                "status": "success",

            },                "profile_id": row[0],

            "Wednesday": {"focus": "Rest or Light Cardio", "exercises": []},                "name": row[1],

            "Thursday": {                "age": row[2],

                "focus": list(exercises_by_part.keys())[2] if len(exercises_by_part) > 2 else "Rest",                "height": row[3],

                "exercises": list(exercises_by_part.values())[2] if len(exercises_by_part) > 2 else [],                "weight": row[4],

            },                "exercise_goal": row[5],

            "Friday": {                "injury": row[6],

                "focus": list(exercises_by_part.keys())[3] if len(exercises_by_part) > 3 else "Rest",            }

                "exercises": list(exercises_by_part.values())[3] if len(exercises_by_part) > 3 else [],        else:

            },            return {"status": "error", "message": "No user profile found in database."}

            "Saturday": {"focus": "Active Recovery or Light Stretching", "exercises": []},    except Exception as e:

            "Sunday": {"focus": "Rest Day", "exercises": []},        return {"status": "error", "message": f"Failed to retrieve profile: {str(e)}"}

        },

    }

    def save_session(user_id: int, user_name: str, profile_data: dict, workout_plan: dict) -> dict:

    if injury and injury.lower() != "none":    """Save a user session with profile and workout plan.

        weekly_plan["injury_modifications"] = (    

            f"⚠️  Important: {profile.get('name')}, you have '{injury}'. "    Args:

            "Please avoid high-impact exercises and consult with a physical therapist. "        user_id: User profile ID from user_profiles table.

            "Low-impact alternatives recommended."        user_name: User's name.

        )        profile_data: Complete user profile dictionary.

            workout_plan: Generated weekly workout plan.

    return weekly_plan        

    Returns:

        Session save status with session ID.

root_agent = Agent(    """

    model="gemini-2.5-flash-lite",    try:

    name="root_agent",        init_sessions_database()

    description="Exercise Planner - Generates personalized weekly workout plans based on user profile and fitness goals.",        conn = sqlite3.connect(SESSIONS_PATH)

    instruction=(        cursor = conn.cursor()

        "You are a friendly Exercise Planner Assistant. Your role is to help users create personalized workout plans.\n\n"        

        "**WORKFLOW:**\n\n"        profile_json = json.dumps(profile_data)

        "**STEP 1: COLLECT USER PROFILE**\n"        plan_json = json.dumps(workout_plan)

        "1. Greet the user warmly\n"        

        "2. Use 'collect_user_profile_form' tool to display the form structure\n"        cursor.execute(

        "3. Collect the user's responses for each field:\n"            """

        "   - Full Name\n"            INSERT INTO sessions (user_id, user_name, profile_data, workout_plan)

        "   - Age (13-120 years)\n"            VALUES (?, ?, ?, ?)

        "   - Height (e.g., 5'10\", 180 cm)\n"            """,

        "   - Weight (50-500 lbs)\n"            (user_id, user_name, profile_json, plan_json),

        "   - Fitness Goal (Weight Loss, Strength Building, or Cardio)\n"        )

        "   - Injuries/Limitations (optional)\n"        conn.commit()

        "4. Present each field one at a time in a friendly manner\n"        session_id = cursor.lastrowid

        "5. Wait for user input before moving to the next field\n\n"        conn.close()

        "**STEP 2: VALIDATE PROFILE**\n"        

        "Once you have all the information:\n"        return {

        "1. Call 'validate_user_profile' with all the collected information\n"            "status": "success",

        "2. If validation fails, ask the user to correct the invalid field\n"            "session_id": session_id,

        "3. If validation succeeds, proceed to STEP 3\n\n"            "user_id": user_id,

        "**STEP 3: GENERATE WORKOUT PLAN**\n"            "message": f"✅ Session saved! Session ID: {session_id}",

        "1. Use 'generate_weekly_workout_plan' tool with the validated profile\n"        }

        "2. Present the weekly schedule clearly with:\n"    except Exception as e:

        "   - Each day's focus area\n"        return {"status": "error", "message": f"Failed to save session: {str(e)}"}

        "   - Specific exercises recommended\n"

        "   - Sets and reps guidance\n"

        "3. Include any injury modifications if needed\n"def get_user_sessions(user_name: str) -> dict:

        "4. Provide recommendations for workout frequency and recovery\n\n"    """Retrieve all sessions for a specific user by name.

        "**IMPORTANT GUIDELINES:**\n"    

        "- Be warm, encouraging, and supportive\n"    Args:

        "- Make the process conversational and easy to follow\n"        user_name: User's name to search for sessions.

        "- Ask clarifying questions if needed\n"        

        "- Provide safety tips and form guidance\n"    Returns:

        "- Remind users to consult a doctor if they have serious injuries\n"        List of sessions with profile and workout plan data.

        "- Suggest proper warm-up and cool-down routines\n"    """

        "- Emphasize the importance of rest days and recovery\n"    try:

        "- Be adaptable to user questions about nutrition, recovery, etc.\n"        init_sessions_database()

    ),        conn = sqlite3.connect(SESSIONS_PATH)

    tools=[        cursor = conn.cursor()

        collect_user_profile_form,        

        validate_user_profile,        cursor.execute(

        generate_weekly_workout_plan,            """

    ],            SELECT session_id, user_id, profile_data, workout_plan, 

)                   refinement_history, created_at, last_updated

            FROM sessions
            WHERE user_name = ?
            ORDER BY last_updated DESC
            """,
            (user_name,),
        )
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            sessions_list = []
            for row in rows:
                sessions_list.append({
                    "session_id": row[0],
                    "user_id": row[1],
                    "profile": json.loads(row[2]),
                    "workout_plan": json.loads(row[3]),
                    "refinement_history": json.loads(row[4]),
                    "created_at": row[5],
                    "last_updated": row[6],
                })
            
            return {
                "status": "success",
                "user_name": user_name,
                "sessions_count": len(sessions_list),
                "sessions": sessions_list,
            }
        else:
            return {
                "status": "not_found",
                "message": f"No sessions found for user '{user_name}'",
            }
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve sessions: {str(e)}"}


def get_latest_user_session(user_name: str) -> dict:
    """Retrieve the most recent session for a user.
    
    Args:
        user_name: User's name to search for the latest session.
        
    Returns:
        Most recent session with profile and workout plan.
    """
    try:
        init_sessions_database()
        conn = sqlite3.connect(SESSIONS_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT session_id, user_id, profile_data, workout_plan, 
                   refinement_history, created_at, last_updated
            FROM sessions
            WHERE user_name = ?
            ORDER BY last_updated DESC
            LIMIT 1
            """,
            (user_name,),
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "status": "success",
                "session_id": row[0],
                "user_id": row[1],
                "profile": json.loads(row[2]),
                "workout_plan": json.loads(row[3]),
                "refinement_history": json.loads(row[4]),
                "created_at": row[5],
                "last_updated": row[6],
            }
        else:
            return {
                "status": "not_found",
                "message": f"No session found for user '{user_name}'",
            }
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve session: {str(e)}"}


def add_refinement_to_session(session_id: int, refinement_type: str, refinement_details: dict) -> dict:
    """Add a refinement request to an existing session's history.
    
    Args:
        session_id: Session ID to update.
        refinement_type: Type of refinement (e.g., 'difficulty_increase', 'focus_change').
        refinement_details: Details about the refinement.
        
    Returns:
        Update status.
    """
    try:
        init_sessions_database()
        conn = sqlite3.connect(SESSIONS_PATH)
        cursor = conn.cursor()
        
        # Get current refinement history
        cursor.execute(
            "SELECT refinement_history FROM sessions WHERE session_id = ?",
            (session_id,),
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return {"status": "error", "message": f"Session {session_id} not found"}
        
        refinement_history = json.loads(row[0])
        
        # Add new refinement
        refinement_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": refinement_type,
            "details": refinement_details,
        }
        refinement_history.append(refinement_entry)
        
        # Update session
        cursor.execute(
            """
            UPDATE sessions
            SET refinement_history = ?, last_updated = CURRENT_TIMESTAMP
            WHERE session_id = ?
            """,
            (json.dumps(refinement_history), session_id),
        )
        conn.commit()
        conn.close()
        
        return {
            "status": "success",
            "session_id": session_id,
            "refinement_count": len(refinement_history),
            "message": f"✅ Refinement logged to session {session_id}",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to add refinement: {str(e)}"}


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


def generate_weekly_workout_plan_from_profile(profile: dict) -> dict:
    """Generates a weekly workout plan based on user profile from database."""
    goal = profile.get("exercise_goal", "Strength Building")
    user_age = profile.get("age", 30)
    injury = profile.get("injury", "None")
    weight = profile.get("weight", 170)
    goal_body_parts = {
        "Weight Loss": ["Abdominals", "Legs", "Back", "Chest"],
        "Strength Building": ["Back", "Chest", "Legs", "Abdominals"],
        "Cardio": ["Abdominals", "Legs", "Cardiovascular"],
    }
    body_parts = goal_body_parts.get(goal, ["Abdominals", "Chest", "Back"])
    difficulty = "Intermediate"
    if user_age < 18 or weight > 250 or user_age > 60:
        difficulty = "Beginner"
    exercises_by_part = get_exercises_by_goal_and_body_part(goal, body_parts, difficulty)
    weekly_plan = {
        "profile_id": profile.get("profile_id"),
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
            "Please avoid high-impact exercises and consult with a physical therapist. "
            "Low-impact alternatives recommended."
        )
    return weekly_plan


root_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="root_agent",
    description="Sequential Exercise Planner - Collects user profile, generates personalized workout plans, and manages session history for refinements.",
    instruction=(
        "You are an Exercise Planner Assistant. Your role is to help users get personalized workout plans and refine them based on feedback.\n\n"
        "**WORKFLOW:**\n\n"
        "**AT START: Check for Existing Sessions**\n"
        "When a user greets you or starts a conversation:\n"
        "1. Ask for their name\n"
        "2. Use 'get_latest_user_session' to check if they have a previous session\n"
        "3. If found: Show their previous profile and plan, ask if they want to refine it or create new\n"
        "4. If not found: Proceed to STEP 1 (new profile)\n\n"
        "**STEP 1: DISPLAY USER PROFILE FORM (New Users Only)**\n"
        "Use the 'collect_user_profile_form' tool to display an interactive form structure.\n"
        "Then collect the user's responses for each field:\n"
        "- Full Name\n"
        "- Age (13-120 years)\n"
        "- Height (e.g., 5'10\", 180 cm)\n"
        "- Weight (50-500 lbs)\n"
        "- Fitness Goal (Weight Loss, Strength Building, or Cardio)\n"
        "- Injuries/Limitations (optional, enter 'None' if no injuries)\n\n"
        "Present each field one at a time in a clear, friendly manner.\n"
        "Wait for the user to provide each input before moving to the next.\n\n"
        "**STEP 2: SAVE THE PROFILE**\n"
        "Once you have collected all fields, call 'save_user_profile' with all the information.\n"
        "The profile will be saved to the database with validation.\n"
        "Confirm successful save with the profile ID and summary.\n\n"
        "**STEP 3: GENERATE PERSONALIZED PLAN**\n"
        "After saving the profile:\n"
        "1. Use 'get_latest_user_profile' to retrieve the saved profile from database\n"
        "2. Use 'generate_weekly_workout_plan_from_profile' to create a personalized weekly plan\n"
        "3. Present the weekly schedule clearly with each day, focus area, and specific exercises\n\n"
        "**STEP 4: SAVE SESSION**\n"
        "After generating the plan:\n"
        "1. Call 'save_session' with the user_id, name, profile, and workout_plan\n"
        "2. Store this session for future refinements\n\n"
        "**STEP 5: PROVIDE GUIDANCE**\n"
        "- Recommend workout frequency based on their goal\n"
        "- Provide safety tips and form guidance\n"
        "- Remind users to consult a doctor if they have serious injuries\n"
        "- Suggest rest days and recovery strategies\n\n"
        "**REFINEMENT WORKFLOW (Returning Users)**\n"
        "If user wants to refine their plan:\n"
        "1. Ask what they want to refine (difficulty, focus, goal change, injury updates)\n"
        "2. Update profile if needed and save new profile\n"
        "3. Generate new plan based on updated profile\n"
        "4. Use 'add_refinement_to_session' to log the refinement\n"
        "5. Save new session or update existing one\n\n"
        "**IMPORTANT NOTES:**\n"
        "- Always start by checking for existing sessions (ask for name first)\n"
        "- For returning users, offer to show their previous plan\n"
        "- Save sessions after every new plan generation\n"
        "- Log refinements to track user's journey\n"
        "- Be friendly, encouraging, and supportive throughout\n"
        "- Make it conversational and easy to understand\n"
    ),
    tools=[
        collect_user_profile_form,
        save_user_profile,
        get_latest_user_profile,
        generate_weekly_workout_plan_from_profile,
        save_session,
        get_user_sessions,
        get_latest_user_session,
        add_refinement_to_session,
    ],
)
