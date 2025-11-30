"""ADK Sequential Agents - Exercise Planner with User Profile Database."""

import csv
import os
import sqlite3
from google.adk.agents.llm_agent import Agent


DATASET_PATH = os.path.join(os.path.dirname(__file__), "megaGymDataset.csv")
DB_PATH = os.path.join(os.path.dirname(__file__), "user_profiles.db")


def init_database():
    """Initialize SQLite database with user profiles table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            height TEXT NOT NULL,
            weight INTEGER NOT NULL,
            exercise_goal TEXT NOT NULL,
            injury TEXT DEFAULT 'None',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_user_profile(
    name: str, age: int, height: str, weight: int, exercise_goal: str, injury: str = "None"
) -> dict:
    """Save user profile to SQLite database."""
    try:
        init_database()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO user_profiles (name, age, height, weight, exercise_goal, injury)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, age, height, weight, exercise_goal, injury),
        )
        conn.commit()
        profile_id = cursor.lastrowid
        conn.close()
        return {
            "status": "success",
            "profile_id": profile_id,
            "message": f"✅ User profile saved! (ID: {profile_id}) Name: {name}, Age: {age}, Goal: {exercise_goal}",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save profile: {str(e)}"}


def get_latest_user_profile() -> dict:
    """Retrieve the most recently created user profile from the database."""
    try:
        init_database()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, age, height, weight, exercise_goal, injury
            FROM user_profiles
            ORDER BY created_at DESC
            LIMIT 1
            """
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "status": "success",
                "profile_id": row[0],
                "name": row[1],
                "age": row[2],
                "height": row[3],
                "weight": row[4],
                "exercise_goal": row[5],
                "injury": row[6],
            }
        else:
            return {"status": "error", "message": "No user profile found in database."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve profile: {str(e)}"}


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
    description="Sequential Exercise Planner - Collects user profile and generates personalized workout plans.",
    instruction=(
        "You are an Exercise Planner Assistant. Your role is to help users get personalized workout plans.\n\n"
        "**WORKFLOW:**\n\n"
        "**STEP 1: COLLECT USER PROFILE**\n"
        "Ask the user for personal information:\n"
        "- Full name (first and last)\n"
        "- Age (in years)\n"
        "- Height (e.g., 5'10\", 180 cm)\n"
        "- Weight (in pounds)\n"
        "- Exercise goal (Weight Loss, Strength Building, or Cardio)\n"
        "- Any injuries or limitations (or 'None')\n\n"
        "Use the 'save_user_profile' tool to save this information to the database.\n\n"
        "**STEP 2: GENERATE PERSONALIZED PLAN**\n"
        "After saving the profile:\n"
        "1. Use 'get_latest_user_profile' to retrieve the saved profile from database\n"
        "2. Use 'generate_weekly_workout_plan_from_profile' to create a personalized weekly plan\n"
        "3. Present the weekly schedule clearly with each day, focus area, and specific exercises\n\n"
        "**STEP 3: PROVIDE GUIDANCE**\n"
        "- Recommend workout frequency based on their goal\n"
        "- Provide safety tips and form guidance\n"
        "- Remind users to consult a doctor if they have serious injuries\n"
        "- Suggest rest days and recovery strategies\n\n"
        "**IMPORTANT NOTES:**\n"
        "- Always follow the sequence: FIRST collect and save profile, THEN retrieve and generate plan\n"
        "- Be friendly, encouraging, and supportive throughout\n"
        "- Make it conversational and easy to understand\n"
        "- Use the database tools to persist user information\n"
    ),
    tools=[
        save_user_profile,
        get_latest_user_profile,
        generate_weekly_workout_plan_from_profile,
    ],
)
