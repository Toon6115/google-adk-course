import asyncio
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import ToolContext
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

# --- State Demo ---
# State lets you store structured key-value data within a session.
# Unlike session history (raw conversation), state is explicit data your tools control.
# Three scopes: session state, user state, and app state.
#
# Prefix conventions:
#   "key"          → session-level (default, scoped to this session only)
#   "user:key"     → user-level (shared across sessions for same user)
#   "app:key"      → app-level (shared across all users and sessions)


def save_preference(key: str, value: str, tool_context: ToolContext) -> dict:
    """Saves a user preference to session state.

    Args:
        key: The preference name (e.g., 'theme', 'language', 'name').
        value: The preference value (e.g., 'dark', 'Python', 'Jani').

    Returns:
        A confirmation dictionary.
    """
    # Store in session state (default scope)
    tool_context.state[key] = value

    # Track known keys so we can list them later
    saved_keys = tool_context.state.get("_saved_keys", [])
    if key not in saved_keys:
        saved_keys.append(key)
    tool_context.state["_saved_keys"] = saved_keys

    return {"status": "saved", "key": key, "value": value}


def get_preference(key: str, tool_context: ToolContext) -> dict:
    """Retrieves a user preference from session state.

    Args:
        key: The preference name to look up.

    Returns:
        A dictionary with the preference value or an error message.
    """
    value = tool_context.state.get(key)
    if value is not None:
        return {"status": "found", "key": key, "value": value}
    return {"status": "not_found", "key": key, "message": f"No preference found for '{key}'."}


def list_preferences(tool_context: ToolContext) -> dict:
    """Lists all saved user preferences from session state.

    Returns:
        A dictionary with all stored preferences.
    """
    # Retrieve the tracked keys and build the preferences dict
    saved_keys = tool_context.state.get("_saved_keys", [])
    prefs = {}
    for k in saved_keys:
        val = tool_context.state.get(k)
        if val is not None:
            prefs[k] = val
    if prefs:
        return {"status": "success", "preferences": prefs}
    return {"status": "empty", "message": "No preferences saved yet."}


# --- Define the Agent ---
agent = Agent(
    name="preferences_agent",
    model="gemini-2.5-flash",
    description="A personal assistant that remembers user preferences using session state.",
    instruction="""You are a personal assistant that manages user preferences.

    You have three tools:
    - save_preference: Save a key-value preference (e.g., name, theme, language)
    - get_preference: Look up a specific preference by key
    - list_preferences: Show all saved preferences

    When the user tells you something about themselves or their preferences,
    proactively save it using save_preference.
    When asked about preferences, retrieve them using the appropriate tool.
    Be friendly and confirm when you save something.""",
    tools=[save_preference, get_preference, list_preferences],
)

# --- Session Service ---
session_service = InMemorySessionService()

APP_NAME = "state_demo"
USER_ID = "user_1"
SESSION_ID = "session_001"

asyncio.run(
    session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
)

runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)


def call_agent(query):
    """Send a message and print the response."""
    print(f"\n>>> User: {query}")
    message = types.Content(role="user", parts=[types.Part(text=query)])

    final_response = "No response received."
    for event in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    print(f"<<< Agent: {final_response}")


# =============================================
# PART 1: Save preferences via conversation
# =============================================
print("=" * 60)
print("PART 1: Saving preferences through conversation")
print("=" * 60)

call_agent("My name is Jani.")
call_agent("I prefer dark mode for all my apps.")
call_agent("My favorite programming language is Python.")
call_agent("Set my timezone to IST.")

# =============================================
# PART 2: Retrieve preferences
# =============================================
print("\n" + "=" * 60)
print("PART 2: Retrieving preferences")
print("=" * 60)

call_agent("What is my name?")
call_agent("What theme do I prefer?")
call_agent("List all my preferences.")

# =============================================
# PART 3: Inspect state directly
# =============================================
print("\n" + "=" * 60)
print("PART 3: Inspecting session state programmatically")
print("=" * 60)

session = asyncio.run(
    session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
)

print("\nSession state contents:")
for key, value in session.state.items():
    if not key.startswith("_"):
        print(f"  {key} = {value}")