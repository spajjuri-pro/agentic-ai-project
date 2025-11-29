"""ADK Agent - Exercise Planner Assistant."""

from google.adk.agents.llm_agent import Agent


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


def generate_exercise_plan(goal: str, user_age: int, injury: str, weight: int) -> dict:
    """Generates a personalized exercise plan based on user's goal and profile.
    
    Args:
        goal: Exercise goal ("Weight Loss", "Strength Building", or "Cardio").
        user_age: User's age in years.
        injury: Any current injuries or limitations.
        weight: User's current weight in pounds.
        
    Returns:
        A dictionary with recommended exercises for the specified goal.
    """
    exercises = {}
    
    if goal == "Weight Loss":
        exercises = {
            "goal": "Weight Loss",
            "exercises": [
                "30 min running or jogging (moderate pace)",
                "Circuit training: 3 sets of 10 reps each (burpees, mountain climbers, jumping jacks)",
                "Swimming: 30-45 min",
                "High-Intensity Interval Training (HIIT): 20 min",
            ],
            "frequency": "5-6 days per week",
            "notes": "Combine cardio with strength training for optimal results.",
        }
    elif goal == "Strength Building":
        exercises = {
            "goal": "Strength Building",
            "exercises": [
                "Squats: 4 sets of 8-10 reps",
                "Deadlifts: 4 sets of 5-8 reps",
                "Bench Press: 4 sets of 8-10 reps",
                "Pull-ups or Lat Pulldowns: 3 sets of 8-12 reps",
                "Rows: 3 sets of 8-10 reps",
            ],
            "frequency": "4-5 days per week",
            "notes": "Rest 48 hours between muscle groups. Focus on compound movements.",
        }
    elif goal == "Cardio":
        exercises = {
            "goal": "Cardio (Stamina Building)",
            "exercises": [
                "Running: 3-5 miles at steady pace",
                "Cycling: 45-60 min moderate intensity",
                "Jump Rope: 5 sets of 2 min intervals",
                "Rowing Machine: 30-45 min",
                "Elliptical: 40-50 min",
            ],
            "frequency": "4-6 days per week",
            "notes": "Gradually increase duration and intensity. Mix steady-state and interval training.",
        }
    else:
        exercises = {
            "status": "error",
            "message": f"Unknown goal: {goal}. Choose 'Weight Loss', 'Strength Building', or 'Cardio'.",
        }
    
    # Add injury-specific modifications
    if injury and injury.lower() != "none":
        exercises["injury_modifications"] = (
            f"Important: You have a '{injury}'. Please consult with a doctor or physical therapist "
            "before starting this exercise plan. Consider low-impact alternatives."
        )
    
    return exercises


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
    description="Exercise Planner - Creates personalized workout plans based on user profile and fitness goals.",
    instruction=(
        "You are a helpful Exercise Planner assistant. Your role is to:\n"
        "1. Collect user information (first name, last name, age, injury, height, weight)\n"
        "2. Determine their fitness goal (Weight Loss, Strength Building, or Cardio)\n"
        "3. Generate personalized exercises using the 'generate_exercise_plan' tool\n"
        "4. Ask for feedback on the exercises using the 'collect_user_feedback' tool\n"
        "Be friendly, encouraging, and always remind users to consult a doctor if they have injuries."
    ),
    tools=[collect_user_info, generate_exercise_plan, collect_user_feedback],
)