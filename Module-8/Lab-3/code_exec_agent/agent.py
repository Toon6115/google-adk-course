from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.code_executors import BuiltInCodeExecutor

from dotenv import load_dotenv
load_dotenv()

# --- Built-in Tool: Code Execution ---
# The BuiltInCodeExecutor lets the agent write and run Python code
# using Gemini's built-in code execution capability.
# This is useful for calculations, data processing, and analysis.

root_agent = Agent(
    name="code_exec_agent",
    model="gemini-2.5-flash",
    description="An agent that can write and execute Python code.",
    instruction="""You are a helpful assistant that can write and execute Python code.
    When given a mathematical problem, data analysis task, or any computation,
    write Python code to solve it.
    Return the result clearly to the user.
    You can also use Google Search for factual information.""",
    tools=[google_search],
    code_executor=BuiltInCodeExecutor(),  # Enable code execution
)
