from google.adk.agents import Agent

from dotenv import load_dotenv
load_dotenv()

# --- Define Function Tools ---
# In ADK, any Python function with type hints and a docstring becomes a tool.
# The LLM uses the function name, docstring, and parameter types to decide when and how to call it.

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city: The name of the city to get the weather for.

    Returns:
        A dictionary containing the weather status and temperature.
    """
    # Mock weather data
    mock_data = {
        "new york": {"status": "success", "report": "Sunny, 72°F (22°C). Light breeze from the west."},
        "london": {"status": "success", "report": "Cloudy, 59°F (15°C). Chance of rain in the evening."},
        "tokyo": {"status": "success", "report": "Clear skies, 68°F (20°C). Humidity at 45%."},
        "paris": {"status": "success", "report": "Partly cloudy, 65°F (18°C). Pleasant conditions."},
        "sydney": {"status": "success", "report": "Warm, 82°F (28°C). UV index is high."},
    }
    city_lower = city.lower().strip()
    if city_lower in mock_data:
        return mock_data[city_lower]
    return {"status": "error", "message": f"Weather data not available for '{city}'."}


def get_temperature_unit_conversion(celsius: float) -> dict:
    """Converts a temperature from Celsius to Fahrenheit and Kelvin.

    Args:
        celsius: The temperature in Celsius to convert.

    Returns:
        A dictionary with the temperature in Fahrenheit and Kelvin.
    """
    fahrenheit = (celsius * 9 / 5) + 32
    kelvin = celsius + 273.15
    return {
        "celsius": celsius,
        "fahrenheit": round(fahrenheit, 2),
        "kelvin": round(kelvin, 2),
    }


# --- Define the Agent with Function Tools ---
root_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    description="A weather assistant that can check weather and convert temperatures.",
    instruction="""You are a helpful weather assistant.
    Use the 'get_weather' tool to check current weather conditions for a city.
    Use the 'get_temperature_unit_conversion' tool to convert temperatures between units.
    Always provide clear and friendly responses.""",
    tools=[get_weather, get_temperature_unit_conversion],  # Pass functions directly as tools
)
