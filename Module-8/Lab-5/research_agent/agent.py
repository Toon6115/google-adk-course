from google.adk.agents import Agent
from google.adk.tools.langchain_tool import LangchainTool

from dotenv import load_dotenv
load_dotenv()

# --- 3rd Party Tools: LangChain Integration ---
# ADK can wrap any LangChain community tool using the LangchainTool wrapper.
# This gives you access to LangChain's massive ecosystem of 100+ tools.
# Here we use Wikipedia as an example.

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Create LangChain Wikipedia tool
wikipedia_lc = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# Wrap it with ADK's LangchainTool wrapper
wikipedia_tool = LangchainTool(
    tool=wikipedia_lc,
    name="wikipedia_search",
    description="Search Wikipedia for information on any topic. Use this for factual, encyclopedic information.",
)

# --- Define the Agent ---
root_agent = Agent(
    name="research_agent",
    model="gemini-2.5-flash",
    description="A research assistant with access to Wikipedia via LangChain tools.",
    instruction="""You are a knowledgeable research assistant.
    Use the Wikipedia tool to look up factual information.
    Provide clear, well-organized answers based on the search results.
    Always indicate when information comes from Wikipedia.""",
    tools=[wikipedia_tool],
)
