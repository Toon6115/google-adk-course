import asyncio
from google.adk.agents import Agent
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import ToolContext
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from typing import Optional, Dict, Any

from dotenv import load_dotenv
load_dotenv()

# --- Tool Callbacks Demo ---
# ADK provides two callback points around tool execution:
#
# 1. before_tool_callback — fires BEFORE each tool runs
#    Signature: (BaseTool, Dict, ToolContext) -> Optional[Dict]
#    Return None → tool executes normally | Return Dict → skip tool, use this as result
#
# 2. after_tool_callback — fires AFTER each tool completes
#    Signature: (BaseTool, Dict, ToolContext, Dict) -> Optional[Dict]
#    Return None → keep original result | Return Dict → replace the result

# --- Tracking data ---
tool_call_log = []
tool_results_log = []

# --- Policy: blocked cities ---
BLOCKED_CITIES = ["paris", "moscow"]


# --- Define tools ---

def get_weather(city: str) -> dict:
    """Gets the current weather for a city.

    Args:
        city: The city name to check weather for.

    Returns:
        A dictionary with weather information.
    """
    weather_data = {
        "new york": {"temp": "22°C", "condition": "Sunny", "humidity": "45%"},
        "london": {"temp": "15°C", "condition": "Cloudy", "humidity": "78%"},
        "tokyo": {"temp": "28°C", "condition": "Clear", "humidity": "60%"},
        "paris": {"temp": "18°C", "condition": "Rainy", "humidity": "85%"},
        "sydney": {"temp": "25°C", "condition": "Partly Cloudy", "humidity": "55%"},
    }
    city_lower = city.lower()
    if city_lower in weather_data:
        return {"status": "success", "city": city, **weather_data[city_lower]}
    return {"status": "error", "message": f"No weather data for '{city}'."}


def get_stock_price(symbol: str) -> dict:
    """Gets the current stock price for a ticker symbol.

    Args:
        symbol: The stock ticker symbol (e.g., AAPL, GOOGL).

    Returns:
        A dictionary with stock price information.
    """
    stock_data = {
        "AAPL": {"price": 189.50, "change": "+1.2%"},
        "GOOGL": {"price": 141.80, "change": "-0.5%"},
        "MSFT": {"price": 378.90, "change": "+0.8%"},
    }
    symbol_upper = symbol.upper()
    if symbol_upper in stock_data:
        return {"status": "success", "symbol": symbol_upper, **stock_data[symbol_upper]}
    return {"status": "error", "message": f"No data for symbol '{symbol}'."}


# =============================================
# CALLBACK 1: Before Tool — Validate & Block
# =============================================
def validate_tool_call(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    """Validates tool arguments and blocks restricted calls."""
    tool_name = tool.name

    log_entry = {
        "tool": tool_name,
        "args": dict(args),
        "blocked": False,
        "reason": None,
    }

    print(f"\n  [BEFORE TOOL] Tool: {tool_name} | Args: {args}")

    # Policy: Block weather for restricted cities
    if tool_name == "get_weather":
        city = args.get("city", "").lower()
        if city in BLOCKED_CITIES:
            log_entry["blocked"] = True
            log_entry["reason"] = f"City '{city}' is restricted."
            tool_call_log.append(log_entry)

            print(f"  [BEFORE TOOL] *** BLOCKED: '{city}' is restricted! ***")

            return {
                "status": "blocked",
                "message": f"Weather data for '{args.get('city')}' is restricted by company policy.",
            }

    print(f"  [BEFORE TOOL] Allowed.")
    tool_call_log.append(log_entry)
    return None


# =============================================
# CALLBACK 2: After Tool — Log & Enrich
# =============================================
def enrich_tool_result(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    """Logs tool results and enriches them with metadata."""
    tool_name = tool.name

    print(f"  [AFTER TOOL] Tool: {tool_name} | Result: {str(tool_response)[:80]}...")

    # Skip logging if the call was blocked by before_tool_callback
    if isinstance(tool_response, dict) and tool_response.get("status") == "blocked":
        print(f"  [AFTER TOOL] Skipped — call was blocked by before_tool_callback.")
        return None

    # Log the result
    tool_results_log.append({
        "tool": tool_name,
        "args": dict(args),
        "status": tool_response.get("status", "unknown") if isinstance(tool_response, dict) else "unknown",
    })

    # Enrich the result with metadata
    if isinstance(tool_response, dict):
        enriched = dict(tool_response)
        enriched["_metadata"] = {
            "processed_by": "after_tool_callback",
            "tool_name": tool_name,
        }
        print(f"  [AFTER TOOL] Enriched with _metadata.")
        return enriched

    return None


# --- Define the Agent with BOTH callbacks ---
agent = Agent(
    name="tool_validator_agent",
    model="gemini-2.5-flash",
    description="A weather and stock assistant with tool validation and result enrichment.",
    instruction="""You are a helpful assistant with access to weather and stock tools.
    When asked about weather, use the get_weather tool.
    When asked about stocks, use the get_stock_price tool.
    Report results clearly and concisely.""",
    tools=[get_weather, get_stock_price],
    before_tool_callback=validate_tool_call,
    after_tool_callback=enrich_tool_result,
)

# --- Session and Runner setup ---
session_service = InMemorySessionService()
APP_NAME = "tool_callbacks_demo"
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
# PART 1: Allowed calls — see both callbacks
# =============================================
print("=" * 60)
print("Tool Callbacks — Validation, Blocking & Result Enrichment")
print("=" * 60)
print("Watch [BEFORE TOOL] validate, then [AFTER TOOL] enrich each result.")

call_agent("What's the weather in Tokyo?")
call_agent("What's the stock price of AAPL?")

# =============================================
# PART 2: Blocked call — before_tool_callback stops it
# =============================================
print("\n" + "=" * 60)
print("Blocked Call — Paris is restricted")
print("=" * 60)

call_agent("What's the weather in Paris?")

# =============================================
# PART 3: Flow continues after a block
# =============================================
print("\n" + "=" * 60)
print("Flow continues normally after a block")
print("=" * 60)

call_agent("What's the weather in London?")

# =============================================
# PART 4: Review audit logs
# =============================================
print("\n" + "=" * 60)
print("Reviewing audit logs")
print("=" * 60)

print(f"\n--- Before Tool Log ---")
print(f"Total tool call attempts: {len(tool_call_log)}")
for i, entry in enumerate(tool_call_log):
    status = "BLOCKED" if entry["blocked"] else "ALLOWED"
    print(f"  {i + 1}. [{status}] {entry['tool']}({entry['args']})")

print(f"\n--- After Tool Log ---")
print(f"Total tool results captured: {len(tool_results_log)}")
for i, entry in enumerate(tool_results_log):
    print(f"  {i + 1}. {entry['tool']}({entry['args']}) → {entry['status']}")

if __name__ == "__main__":
    pass