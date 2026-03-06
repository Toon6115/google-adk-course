import asyncio
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

# --- Sessions Demo ---
# Sessions track conversation history between a user and an agent.
# Each session is identified by three keys: app_name, user_id, session_id.
# The agent automatically remembers previous messages within a session.

agent = Agent(
    name="session_agent",
    model="gemini-2.5-flash",
    description="A helpful assistant that demonstrates session-based memory.",
    instruction="""You are a friendly and concise assistant.
    Answer user questions clearly.
    When asked to recall previous conversation, use the conversation history available to you.""",
)

# --- Session Service ---
session_service = InMemorySessionService()

APP_NAME = "session_demo"
USER_ID = "user_1"


def call_agent(runner, user_id, session_id, query):
    """Send a message and print the response."""
    print(f"\n>>> User: {query}")
    message = types.Content(role="user", parts=[types.Part(text=query)])

    final_response = "No response received."
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=message):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    print(f"<<< Agent: {final_response}")


# =============================================
# PART 1: Multi-turn conversation in ONE session
# =============================================
print("=" * 60)
print("PART 1: Multi-turn conversation (same session)")
print("=" * 60)

SESSION_1 = "session_001"
asyncio.run(
    session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_1
    )
)

runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

# Turn 1: Establish context
call_agent(runner, USER_ID, SESSION_1, "My name is Jani and I live in Hyderabad.")

# Turn 2: Agent should remember the name
call_agent(runner, USER_ID, SESSION_1, "What is my name?")

# Turn 3: Agent should remember the city
call_agent(runner, USER_ID, SESSION_1, "What city do I live in?")

# Turn 4: Agent should recall the full conversation
call_agent(runner, USER_ID, SESSION_1, "Summarize everything we've discussed so far.")


# =============================================
# PART 2: New session = fresh start
# =============================================
print("\n" + "=" * 60)
print("PART 2: New session (context is lost)")
print("=" * 60)

SESSION_2 = "session_002"
asyncio.run(
    session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_2
    )
)

# The agent has NO memory of Session 1
call_agent(runner, USER_ID, SESSION_2, "What is my name?")

call_agent(runner, USER_ID, SESSION_2, "What city do I live in?")

call_agent(runner, USER_ID, SESSION_2, "Summarize everything we've discussed so far.")
