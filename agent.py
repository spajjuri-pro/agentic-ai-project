"""ADK Agent - Exercise Planner Assistant with CSV-based Workout Suggestions."""

import csv
import os
from google.adk.agents.llm_agent import Agent


# Path to the gym dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), "megaGymDataset.csv")


def load_gym_dataset() -> list:
    """Load exercises from the CSV dataset.
    
    Returns:
        A list of dictionaries containing exercise data.
    """
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
    """Filters exercises from the dataset based on goal and body parts.
    
    Args:
        goal: Fitness goal ("Weight Loss", "Strength Building", or "Cardio").
        body_parts: List of body parts to target (e.g., ["Abdominals", "Legs"]).
        difficulty: Exercise difficulty level ("Beginner", "Intermediate", "Expert").
        
    Returns:
        A dictionary with filtered exercises organized by body part.
    """
    exercises = load_gym_dataset()
    filtered = {}
    
    # Map goals to exercise types
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
            # Take top 5 exercises per body part
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


def generate_weekly_workout_plan(
    goal: str,
    user_age: int,
    injury: str,
    weight: int,
    difficulty: str = "Intermediate",
) -> dict:
    """Generates a personalized weekly workout plan using the gym dataset.
    
    Args:
        goal: Exercise goal ("Weight Loss", "Strength Building", or "Cardio").
        user_age: User's age in years.
        injury: Any current injuries or limitations.
        weight: User's current weight in pounds.
        difficulty: Exercise difficulty level ("Beginner", "Intermediate", "Expert").
        
    Returns:
        A dictionary with a weekly workout plan.
    """
    # Determine target body parts based on goal
    goal_body_parts = {
        "Weight Loss": ["Abdominals", "Legs", "Back", "Chest"],
        "Strength Building": ["Back", "Chest", "Legs", "Abdominals"],
        "Cardio": ["Abdominals", "Legs", "Cardiovascular"],
    }
    
    body_parts = goal_body_parts.get(goal, ["Abdominals", "Chest", "Back"])
    
    # Adjust difficulty based on age and current weight
    if user_age < 18:
        difficulty = "Beginner"
    elif weight > 250:
        difficulty = "Beginner"
    
    # Get exercises
    exercises_by_part = get_exercises_by_goal_and_body_part(goal, body_parts, difficulty)
    
    # Build weekly plan
    weekly_plan = {
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
                "exercises": list(exercises_by_part.values())[1]
                if len(exercises_by_part) > 1
                else [],
            },
            "Wednesday": {"focus": "Rest or Light Cardio", "exercises": []},
            "Thursday": {
                "focus": list(exercises_by_part.keys())[2] if len(exercises_by_part) > 2 else "Rest",
                "exercises": list(exercises_by_part.values())[2]
                if len(exercises_by_part) > 2
                else [],
            },
            "Friday": {
                "focus": list(exercises_by_part.keys())[3] if len(exercises_by_part) > 3 else "Rest",
                "exercises": list(exercises_by_part.values())[3]
                if len(exercises_by_part) > 3
                else [],
            },
            "Saturday": {"focus": "Active Recovery or Light Stretching", "exercises": []},
            "Sunday": {"focus": "Rest Day", "exercises": []},
        },
    }
    
    # Add injury modifications
    if injury and injury.lower() != "none":
        weekly_plan["injury_modifications"] = (
            f"⚠️  Important: You have '{injury}'. Please avoid high-impact exercises "
            "and consult with a physical therapist. Low-impact alternatives recommended."
        )
    
    return weekly_plan


def collect_user_info(
    first_name: str, last_name: str, age: int, injury: str, height: str, weight: int
) -> dict:
    """Collects personal information from the user for exercise planning.
    
    Args:
        first_name: User's first name.
        last_name: User's last name.
        age: User's age in years.
        injury: Any current injuries or limitations (e.g., "None", "Knee pain", "Back strain").
        height: User's height (e.g., "5'10\"", "180 cm").
        weight: User's weight in pounds.
        
    Returns:
        A dictionary with collected user information.
    """
    return {
        "status": "success",
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "injury": injury,
        "height": height,
        "weight": weight,
        "message": f"User profile created for {first_name} {last_name}",
    }


def collect_user_feedback(liked_exercises: bool, feedback: str = "") -> dict:
    """Collects user feedback on the exercise plan.
    
    Args:
        liked_exercises: Whether the user liked the recommended exercises (True/False).
        feedback: Optional detailed feedback from the user.
        
    Returns:
        A dictionary confirming feedback has been recorded.
    """
    return {
        "status": "success",
        "liked_exercises": liked_exercises,
        "feedback": feedback,
        "message": "Thank you for your feedback! We'll use this to improve future recommendations.",
    }


root_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="root_agent",
    description="Exercise Planner - Creates personalized workout plans based on user profile, fitness goals, and a database of real exercises.",
    instruction=(
        "You are a helpful Exercise Planner assistant. Your role is to:\n"
        "1. Collect user information (first name, last name, age, injury, height, weight)\n"
        "2. Determine their fitness goal (Weight Loss, Strength Building, or Cardio)\n"
        "3. Generate a personalized WEEKLY workout plan using the 'generate_weekly_workout_plan' tool\n"
        "4. Present the weekly schedule with specific exercises from a professional gym database\n"
        "5. Ask for feedback on the exercises using the 'collect_user_feedback' tool\n"
        "Be friendly, encouraging, and always remind users to consult a doctor if they have injuries.\n"
        "Format the weekly plan clearly with days, exercise names, and repetitions."
    ),
    tools=[
        collect_user_info,
        generate_weekly_workout_plan,
        collect_user_feedback,
        get_exercises_by_goal_and_body_part,
    ],
)