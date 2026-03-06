from google.adk.agents import Agent
from google.adk.tools import google_search

from dotenv import load_dotenv
load_dotenv()

# --- Built-in Tool: Google Search ---
# ADK provides pre-built tools that integrate directly with Gemini's capabilities.
# `google_search` is a built-in tool — no function definition needed.
# It lets the agent perform real Google searches to get up-to-date information.

root_agent = Agent(
    name="search_agent",
    model="gemini-2.5-flash",
    description="An agent that can search the web using Google Search.",
    instruction="""You are a helpful research assistant.
    Use Google Search to find current, accurate information for the user's questions.
    Always cite your sources when possible.
    If you're unsure about something, search for it rather than guessing.""",
    tools=[google_search],  # Built-in tool — just import and use
)
