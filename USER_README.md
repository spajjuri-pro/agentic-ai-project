# Exercise Planner - User Guide

Welcome! This is your guide to using the AI Exercise Planner.

## What is This?

The Exercise Planner is an AI-powered application that creates personalized workout routines based on your fitness profile and goals. It uses machine learning to suggest exercises from a database of 1000+ gym exercises tailored to your needs.

## How to Use

### Step 1: Start the Application

Your administrator should have set up the server. The web interface will be available at:

```
http://localhost:8000
```

### Step 2: Create Your Fitness Profile

When you first use the application, you'll be asked to provide:

- **Full Name** — Your first and last name
- **Age** — Your current age (13-120 years)
- **Height** — How tall you are (e.g., 5'10", 180 cm)
- **Weight** — Your current weight (50-500 lbs)
- **Fitness Goal** — Choose one:
  - Weight Loss
  - Strength Building
  - Cardio
- **Injuries/Limitations** — Any physical limitations to consider (optional)

### Step 3: Get Your Personalized Workout Plan

Once you provide your profile, the AI will generate a complete weekly workout plan customized for you, including:

- **Daily Schedule** — Which exercises to do each day
- **Exercise Details** — Specific exercises with equipment needed
- **Difficulty Level** — Workouts adjusted for your fitness level
- **Rest Days** — Recovery recommendations

## Example Interaction

```
You: "Create a workout plan for me"

App: "Welcome! I'll help you create a personalized workout plan. 
      Let me gather some information about you first.
      
      What's your full name?"

You: "John Smith"

App: "Nice to meet you, John! How old are you?"

You: "35"

App: "What's your height?"

You: "5'10""

App: "What's your current weight in pounds?"

You: "180"

App: "What's your primary fitness goal?
      - Weight Loss
      - Strength Building
      - Cardio"

You: "Weight Loss"

App: "Do you have any injuries or physical limitations?"

You: "None"

App: "Perfect! Here's your personalized weekly workout plan:

     📋 YOUR PERSONALIZED WEEKLY WORKOUT PLAN
     Goal: Weight Loss | Difficulty: Intermediate

     MONDAY - Cardio & Abdominals
     • Burpees - 3 sets of 15 reps
     • Jump Rope - 3 sets of 1 minute
     • Mountain Climbers - 3 sets of 20 reps

     TUESDAY - Legs & Glutes
     • Squats - 4 sets of 12 reps
     • Leg Press - 3 sets of 15 reps
     • Lunges - 3 sets of 12 each leg

     ... (continues through Sunday)
     
     💡 Recovery Tips:
     - Drink plenty of water
     - Get 7-9 hours of sleep
     - Consider foam rolling for recovery"
```

## Features

### 1. Personalized Plans
The AI learns your fitness level based on your age and weight, then customizes difficulty accordingly.

### 2. Goal-Focused
Plans are specifically tailored to your fitness goal:
- **Weight Loss** → More cardio and high-rep exercises
- **Strength Building** → Lower reps, heavier weights
- **Cardio** → Running, jumping, and aerobic exercises

### 3. Injury Aware
Tell the AI about any injuries, and it will avoid exercises that could aggravate them.

### 4. Complete Information
Each exercise includes:
- Exercise name
- Equipment needed
- Number of sets and reps
- Difficulty level

## Tips for Success

### Before Starting
- Make sure you have proper workout space
- Get any needed equipment (dumbbells, mat, etc.)
- Wear appropriate workout clothing and shoes

### During Workouts
- Start with the suggested difficulty level
- If an exercise feels too easy, increase reps or weight
- If it feels too hard, reduce reps or weight
- Always warm up before exercising
- Cool down and stretch after

### After Each Session
- Record how you felt
- Note any exercises that were particularly challenging
- Stay hydrated and eat protein within 30 minutes

## Frequently Asked Questions

**Q: Can I modify the plan?**
A: Create a new profile with different goals or fitness level to get a modified plan.

**Q: What if I don't have certain equipment?**
A: The AI will suggest alternative exercises based on available equipment.

**Q: How often should I do these workouts?**
A: Follow the daily schedule provided. Most plans include 5-6 workout days with 1-2 rest days.

**Q: Can I use this plan multiple times?**
A: Yes! Your profile is saved, so you can request updated plans anytime.

**Q: Do I need a gym membership?**
A: No, the app can suggest bodyweight exercises and exercises you can do at home.

## Support

If you have questions:
1. Check the [Web UI Guide](./WEB_UI_GUIDE.md) for troubleshooting
2. Contact your administrator
3. See [README.md](./README.md) for general information

## Safety Disclaimer

This application provides exercise suggestions based on your profile. However:
- Consult a doctor before starting a new exercise program
- Listen to your body and stop if you experience pain
- Don't ignore injuries or physical limitations
- If you have health conditions, talk to a healthcare provider first

---

**Last Updated:** November 30, 2025

Enjoy your personalized fitness journey! 💪
