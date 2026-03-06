from google.adk.agents import Agent
from google.adk.tools.crewai_tool import CrewaiTool

from dotenv import load_dotenv
load_dotenv()

# --- 3rd Party Tools: CrewAI Integration ---
# ADK can also wrap CrewAI tools using the CrewaiTool wrapper.
# CrewAI provides tools for web scraping, file operations, and more.
# Here we demonstrate wrapping a CrewAI ScrapeWebsiteTool.

from crewai_tools import ScrapeWebsiteTool

# Create the CrewAI tool
crewai_scraper = ScrapeWebsiteTool()

# Wrap it with ADK's CrewaiTool wrapper
scrape_tool = CrewaiTool(
    tool=crewai_scraper,
    name="scrape_website",
    description="Scrape and extract text content from any website URL. Use this to read articles, blog posts, or any web page content.",
)

# --- Define the Agent ---
root_agent = Agent(
    name="web_reader_agent",
    model="gemini-2.5-flash",
    description="An agent that can read and summarize web pages using CrewAI's scraping tool.",
    instruction="""You are a web content analyst.
    Use the scrape_website tool to read content from URLs provided by the user.
    After scraping, provide a clear summary of the page content.
    If the user asks about a specific topic on the page, focus on that.
    Always mention the source URL in your response.""",
    tools=[scrape_tool],
)
