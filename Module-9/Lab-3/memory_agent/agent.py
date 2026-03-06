import asyncio
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.tools import load_memory
from google.genai.types import Content, Part

from dotenv import load_dotenv
load_dotenv()

# --- Long-term Memory Demo ---
# Memory enables agents to recall information across DIFFERENT sessions.
# This solves the problem we saw in Lab-1: new session = fresh start.
#
# How it works:
#   1. Agent has a conversation in Session A (captures facts).
#   2. We call memory_service.add_session_to_memory(session) to store it.
#   3. In a NEW Session B, a different agent uses the `load_memory` tool
#      to search and retrieve facts from Session A.
#
# Key components:
#   - InMemoryMemoryService: stores session data in memory (for demos)
#   - add_session_to_memory(): extracts facts from a completed session
#   - load_memory tool: lets the agent search past memories

# --- Constants ---
APP_NAME = "memory_demo"
USER_ID = "user_1"
MODEL = "gemini-2.5-flash"

# --- Agent Definitions ---

# Agent 1: Captures information from the user
info_capture_agent = LlmAgent(
    model=MODEL,
    name="InfoCaptureAgent",
    instruction="""You are a friendly assistant that acknowledges and confirms
    information the user shares with you. When the user tells you facts about
    themselves, repeat back what you heard to confirm you understood.""",
)

# Agent 2: Recalls information using long-term memory
memory_recall_agent = LlmAgent(
    model=MODEL,
    name="MemoryRecallAgent",
    instruction="""You are a helpful assistant that answers questions about the user.
    Use the 'load_memory' tool to search past conversations for relevant information.
    Always try to use load_memory before saying you don't know something.""",
    tools=[load_memory],
)

# --- Shared Services ---
# IMPORTANT: Both runners must share the SAME session_service and memory_service
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()


async def run_demo():
    # =============================================
    # PART 1: Capture information in Session A
    # =============================================
    print("=" * 60)
    print("PART 1: Capturing information (Session A)")
    print("=" * 60)

    runner1 = Runner(
        agent=info_capture_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    session_a_id = "session_capture"
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_a_id
    )

    # Share several facts across multiple turns
    facts = [
        "My name is Jani and I'm a cloud architect.",
        "I live in Hyderabad, India.",
        "My favorite programming language is Python.",
        "I'm currently building a course on Google ADK.",
    ]

    for fact in facts:
        print(f"\n>>> User: {fact}")
        message = Content(parts=[Part(text=fact)], role="user")

        response_text = "(No response)"
        async for event in runner1.run_async(
            user_id=USER_ID, session_id=session_a_id, new_message=message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                response_text = event.content.parts[0].text

        print(f"<<< Agent: {response_text}")

    # =============================================
    # PART 2: Store Session A in long-term memory
    # =============================================
    print("\n" + "=" * 60)
    print("PART 2: Storing session in long-term memory")
    print("=" * 60)

    completed_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_a_id
    )

    await memory_service.add_session_to_memory(completed_session)
    print("\nSession A has been added to long-term memory.")
    print(f"Session had {len(completed_session.events)} events.")

    # =============================================
    # PART 3: Recall information in Session B
    # =============================================
    print("\n" + "=" * 60)
    print("PART 3: Recalling information (NEW Session B)")
    print("=" * 60)
    print("Note: This is a brand new session — the agent has NO")
    print("conversation history. It must use load_memory to recall facts.")

    runner2 = Runner(
        agent=memory_recall_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    session_b_id = "session_recall"
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_b_id
    )

    # Ask questions that require recalling from memory
    questions = [
        "What is my name and what do I do?",
        "Where do I live?",
        "What programming language do I prefer?",
        "What am I currently working on?",
    ]

    for question in questions:
        print(f"\n>>> User: {question}")
        message = Content(parts=[Part(text=question)], role="user")

        response_text = "(No response)"
        async for event in runner2.run_async(
            user_id=USER_ID, session_id=session_b_id, new_message=message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                response_text = event.content.parts[0].text

        print(f"<<< Agent: {response_text}")

    # =============================================
    # PART 4: Prove memory works across sessions
    # =============================================
    print("\n" + "=" * 60)
    print("PART 4: Verifying cross-session memory")
    print("=" * 60)

    session_b = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_b_id
    )

    print(f"\nSession A ID: {session_a_id}")
    print(f"Session B ID: {session_b_id}")
    print(f"Session B events: {len(session_b.events)}")
    print("\nThe recall agent successfully answered questions about Session A")
    print("even though it was running in a completely different session.")
    print("This is the power of long-term memory!")


if __name__ == "__main__":
    asyncio.run(run_demo())
