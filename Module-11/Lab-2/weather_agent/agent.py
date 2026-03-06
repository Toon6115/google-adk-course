from google.adk.agents import Agent


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
        "hyderabad": {"temp": "35°C", "condition": "Hot", "humidity": "40%"},
    }
    city_lower = city.lower()
    if city_lower in weather_data:
        return {"status": "success", "city": city, **weather_data[city_lower]}
    return {"status": "error", "message": f"No weather data available for '{city}'."}


root_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    description="Provides weather information for cities around the world.",
    instruction="""You are a helpful weather assistant.
    When the user asks for weather in a city, use the get_weather tool.
    Present the results clearly. If the city is not found, let the user know politely.""",
    tools=[get_weather],
)
