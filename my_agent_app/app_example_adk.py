"""App Example - Using ADK InMemorySessionService with the Exercise Planner."""

import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai.types import Content, Part

# Import your agent
from my_agent_app.agent_adk_sessions import root_agent


async def main():
    """Example: Run exercise planner with ADK session management."""
    
    # Step 1: Initialize SessionService
    print("🚀 Initializing ADK SessionService...")
    session_service = InMemorySessionService()
    
    # Step 2: Define application parameters
    app_name = "my_agent_app"
    user_id = "user_alice"
    session_id = "session_001"
    
    # Step 3: Create session (Runner handles this, but shown for clarity)
    print(f"\n📝 Creating session for {user_id}...")
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state={}  # Start with empty state
    )
    print(f"✅ Session created: {session.id}")
    print(f"   Initial state: {session.state}")
    
    # Step 4: Initialize Runner
    print("\n⚙️ Initializing Runner...")
    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service,
    )
    print("✅ Runner initialized")
    
    # Step 5: Simulate conversation turns
    print("\n" + "="*70)
    print("Starting conversation with agent...")
    print("="*70)
    
    # Turn 1: User greets
    print("\n👤 User: Hello, I'd like a workout plan")
    user_message_1 = Content(parts=[Part(text="Hello, I'd like a workout plan")])
    
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message_1,
    ):
        if event.is_final_response():
            print(f"\n🤖 Agent: {event.content}")
    
    # Check session state after turn 1
    updated_session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    print(f"\n📊 Session state after Turn 1:")
    print(f"   Keys: {list(updated_session.state.keys())}")
    
    # Turn 2: User provides profile info (simulated)
    print("\n👤 User: My name is Alice, I'm 28 years old, 5'7\", 150 lbs, and want to build strength")
    user_message_2 = Content(parts=[
        Part(text="My name is Alice, I'm 28 years old, 5'7\", 150 lbs, and want to build strength")
    ])
    
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message_2,
    ):
        if event.is_final_response():
            print(f"\n🤖 Agent: {event.content}")
    
    # Check session state after turn 2
    updated_session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    print(f"\n📊 Session state after Turn 2:")
    for key, value in updated_session.state.items():
        if not key.startswith("temp:"):
            print(f"   {key}: {value}")
    
    # Turn 3: User asks for refinement
    print("\n👤 User: That plan looks good, but can you make it more challenging?")
    user_message_3 = Content(parts=[
        Part(text="That plan looks good, but can you make it more challenging?")
    ])
    
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message_3,
    ):
        if event.is_final_response():
            print(f"\n🤖 Agent: {event.content}")
    
    # Final session state
    final_session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    print("\n" + "="*70)
    print("FINAL SESSION STATE")
    print("="*70)
    print(f"\nSession ID: {final_session.id}")
    print(f"User ID: {final_session.user_id}")
    print(f"App: {final_session.app_name}")
    print(f"Total events: {len(final_session.events)}")
    print(f"\nState contents:")
    for key, value in final_session.state.items():
        if isinstance(value, dict):
            print(f"  {key}: <dict with {len(value)} keys>")
        elif isinstance(value, list):
            print(f"  {key}: <list with {len(value)} items>")
        else:
            print(f"  {key}: {value}")
    
    print("\n✅ Conversation complete!")
    print("   All data persisted in session.state")
    print("   User-scoped data (user:*) will be available in future sessions")
    
    # Cleanup
    await session_service.delete_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    print("\n🧹 Session cleaned up")


async def example_session_retrieval():
    """Example: Retrieve and resume a session (returning user)."""
    
    print("\n" + "="*70)
    print("EXAMPLE: SESSION RETRIEVAL FOR RETURNING USER")
    print("="*70)
    
    # Initialize
    session_service = InMemorySessionService()
    app_name = "my_agent_app"
    user_id = "user_bob"
    
    # Create first session
    session1 = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        state={
            "user:name": "Bob",
            "user:age": 35,
            "current_workout_plan": {"Monday": "Chest day"}
        }
    )
    print(f"\n✅ Created Session 1: {session1.id}")
    
    # List all sessions for user
    sessions = await session_service.list_sessions(app_name=app_name, user_id=user_id)
    print(f"\n📋 Found {len(sessions)} session(s) for {user_id}:")
    for s in sessions:
        print(f"   - Session {s.id}: Created at {s.last_update_time}")
    
    # Get most recent
    latest_session = sessions[0]
    print(f"\n🔄 Retrieved latest session: {latest_session.id}")
    print(f"   User name: {latest_session.state.get('user:name')}")
    print(f"   Last workout: {latest_session.state.get('current_workout_plan', {}).get('Monday')}")
    
    print("\n✅ This is how you retrieve sessions for returning users!")


if __name__ == "__main__":
    # Run main conversation example
    asyncio.run(main())
    
    # Run retrieval example
    # asyncio.run(example_session_retrieval())
    
    print("\n" + "="*70)
    print("To test session retrieval, uncomment the example_session_retrieval() call")
    print("="*70)

