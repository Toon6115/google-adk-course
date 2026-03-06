import asyncio
import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines
from google.genai.types import Content, Part

from dotenv import load_dotenv
load_dotenv()

# --- Test Agent Engine Deployment ---
# This script connects to the agent deployed in Lab-2 and interacts with it
# using the Python SDK.
#
# Prerequisites:
#   - Agent deployed via Lab-2 (adk deploy agent_engine)
#   - GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION set
#   - gcloud auth application-default login completed

# ============================================
# STEP 1: Configuration
# ============================================
print("=" * 60)
print("STEP 1: Initializing...")
print("1. PROJECT_ID")
print("2. LOCATION")
print("3. RESOURCE_NAME")
print("=" * 60)

# Replace with your values from Lab-2
PROJECT_ID = ""
LOCATION = ""
RESOURCE_NAME = ""
# Or just the resource ID: RESOURCE_ID = "1234567890"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)


async def main():
    # ============================================
    # STEP 2: Connect to the deployed agent
    # ============================================
    print("=" * 60)
    print("STEP 2: Connecting to Agent Engine")
    print("=" * 60)

    remote_app = agent_engines.get(RESOURCE_NAME)
    print(f"Connected to: {remote_app}")

    # ============================================
    # STEP 3: Create a session
    # ============================================
    print("\n" + "=" * 60)
    print("STEP 3: Creating a session")
    print("=" * 60)

    session = await remote_app.async_create_session(user_id="demo_user")
    session_id = session["id"]
    print(f"Session created: {session_id}")
    print(f"Full session object: {session}")

    # ============================================
    # STEP 4: Send messages
    # ============================================
    print("\n" + "=" * 60)
    print("STEP 4: Chatting with the agent")
    print("=" * 60)

    queries = [
        "What's the weather in Tokyo?",
        "How about London?",
        "Which city is warmer?",
    ]

    for query in queries:
        print(f"\n>>> User: {query}")

        response = remote_app.async_stream_query(
            user_id="demo_user",
            session_id=session_id,
            message=query,
        )

        # Collect streaming response — extract just the text
        full_response = ""
        async for chunk in response:
            # Response chunks are dicts with content.parts[].text
            content = chunk.get("content") if isinstance(chunk, dict) else getattr(chunk, "content", None)
            if content:
                parts = content.get("parts") if isinstance(content, dict) else getattr(content, "parts", [])
                for part in (parts or []):
                    text = part.get("text") if isinstance(part, dict) else getattr(part, "text", None)
                    if text:
                        full_response += text

        if full_response:
            print(f"<<< Agent: {full_response}")

    # ============================================
    # STEP 5: List all deployed agents
    # ============================================
    print("\n" + "=" * 60)
    print("STEP 5: Listing all deployed agents")
    print("=" * 60)

    agents = agent_engines.list()
    for agent in agents:
        print(f"  - {agent.display_name} ({agent.resource_name})")

    # ============================================
    # STEP 6: Cleanup (optional)
    # ============================================
    print("\n" + "=" * 60)
    print("STEP 6: Cleanup")
    print("=" * 60)
    print("To delete the deployed agent, uncomment the line below:")
    print("  # remote_app.delete()")
    # remote_app.delete()
    # print("Agent deleted.")

    print("\nDone! The agent is running on Agent Engine.")


if __name__ == "__main__":
    asyncio.run(main())
