"""
Weather Assistant Agent - OpenAPI Tools Demonstration

This agent demonstrates how to use OpenAPIToolset to interact with the
OpenWeatherMap API for weather information retrieval.
"""

from google.adk.agents import Agent
from google.adk.tools.openapi_tool import OpenAPIToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
import os

# ============================================================================
# OPENAPI SPECIFICATION
# ============================================================================

# OpenWeatherMap API OpenAPI Specification
# Based on: https://openweathermap.org/api
WEATHER_API_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "OpenWeatherMap API",
        "description": "Weather data API for current weather and forecasts",
        "version": "2.5.0"
    },
    "servers": [
        {
            "url": "https://api.openweathermap.org/data/2.5"
        }
    ],
    "paths": {
        "/weather": {
            "get": {
                "operationId": "get_current_weather",
                "summary": "Get current weather",
                "description": "Returns current weather data for a specified location.",
                "parameters": [
                    {
                        "name": "q",
                        "in": "query",
                        "description": "City name, state code (US only), and country code divided by comma (e.g., 'London,UK' or 'Paris,FR')",
                        "required": False,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "lat",
                        "in": "query",
                        "description": "Latitude",
                        "required": False,
                        "schema": {
                            "type": "number"
                        }
                    },
                    {
                        "name": "lon",
                        "in": "query",
                        "description": "Longitude",
                        "required": False,
                        "schema": {
                            "type": "number"
                        }
                    },
                    {
                        "name": "units",
                        "in": "query",
                        "description": "Units of measurement (standard, metric, imperial)",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "enum": ["standard", "metric", "imperial"],
                            "default": "metric"
                        }
                    },
                    {
                        "name": "appid",
                        "in": "query",
                        "description": "API key",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "coord": {
                                            "type": "object",
                                            "properties": {
                                                "lon": {"type": "number"},
                                                "lat": {"type": "number"}
                                            }
                                        },
                                        "weather": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "integer"},
                                                    "main": {"type": "string"},
                                                    "description": {"type": "string"},
                                                    "icon": {"type": "string"}
                                                }
                                            }
                                        },
                                        "main": {
                                            "type": "object",
                                            "properties": {
                                                "temp": {"type": "number"},
                                                "feels_like": {"type": "number"},
                                                "temp_min": {"type": "number"},
                                                "temp_max": {"type": "number"},
                                                "pressure": {"type": "integer"},
                                                "humidity": {"type": "integer"}
                                            }
                                        },
                                        "wind": {
                                            "type": "object",
                                            "properties": {
                                                "speed": {"type": "number"},
                                                "deg": {"type": "integer"}
                                            }
                                        },
                                        "clouds": {
                                            "type": "object",
                                            "properties": {
                                                "all": {"type": "integer"}
                                            }
                                        },
                                        "name": {"type": "string"},
                                        "sys": {
                                            "type": "object",
                                            "properties": {
                                                "country": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/forecast": {
            "get": {
                "operationId": "get_weather_forecast",
                "summary": "Get 5 day weather forecast",
                "description": "Returns 5 day weather forecast with data every 3 hours.",
                "parameters": [
                    {
                        "name": "q",
                        "in": "query",
                        "description": "City name, state code, and country code",
                        "required": False,
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "name": "lat",
                        "in": "query",
                        "description": "Latitude",
                        "required": False,
                        "schema": {
                            "type": "number"
                        }
                    },
                    {
                        "name": "lon",
                        "in": "query",
                        "description": "Longitude",
                        "required": False,
                        "schema": {
                            "type": "number"
                        }
                    },
                    {
                        "name": "units",
                        "in": "query",
                        "description": "Units of measurement",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "enum": ["standard", "metric", "imperial"],
                            "default": "metric"
                        }
                    },
                    {
                        "name": "cnt",
                        "in": "query",
                        "description": "Number of timestamps to return (max 40)",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 40
                        }
                    },
                    {
                        "name": "appid",
                        "in": "query",
                        "description": "API key",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "list": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "dt": {"type": "integer"},
                                                    "main": {"type": "object"},
                                                    "weather": {"type": "array"},
                                                    "wind": {"type": "object"},
                                                    "dt_txt": {"type": "string"}
                                                }
                                            }
                                        },
                                        "city": {
                                            "type": "object",
                                            "properties": {
                                                "name": {"type": "string"},
                                                "country": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

# ============================================================================
# OPENAPI TOOLSET WITH AUTHENTICATION
# ============================================================================

# Get OpenWeatherMap API key from environment
weather_api_key = os.getenv("OPENWEATHER_API_KEY")

if not weather_api_key:
    print("WARNING: OPENWEATHER_API_KEY not found in environment variables.")
    print("Please set OPENWEATHER_API_KEY in your .env file to use this agent.")
    print("Get your free API key at: https://openweathermap.org/api")
    weather_api_key = "demo_key"  # Placeholder

# Create OpenAPIToolset - OpenWeatherMap uses API key in query params
# No special auth header needed, the API key is passed as a query parameter
weather_toolset = OpenAPIToolset(
    spec_dict=WEATHER_API_SPEC,
    # OpenWeatherMap doesn't use header auth, API key is in query params
    # So we don't need auth_scheme/auth_credential here
)

# ============================================================================
# AGENT DEFINITION
# ============================================================================

weather_agent = Agent(
    name="weather_assistant",
    model="gemini-2.0-flash",

    description="""
    Weather assistant that provides current weather information and forecasts
    for any location worldwide using the OpenWeatherMap API.
    """,

    instruction=f"""
    You are a helpful weather assistant! You can provide current weather information
    and 5-day forecasts for any location in the world.

    CAPABILITIES:
    - Get current weather for any city or coordinates
    - Get 5-day weather forecast with 3-hour intervals
    - Support multiple units (metric, imperial, standard)
    - Provide detailed weather information including temperature, humidity, wind, etc.

    IMPORTANT NOTES:
    - ALWAYS include the API key parameter: appid="{weather_api_key}"
    - Default to metric units (Celsius) unless user specifies otherwise
    - For city names, use format: "CityName,CountryCode" (e.g., "London,UK", "Paris,FR")
    - Be conversational and friendly in your responses
    - Explain weather conditions in easy-to-understand terms
    - Provide helpful context (e.g., "It's quite cold, dress warmly!")

    RESPONSE STYLE:
    - Start with a friendly greeting if it's the first message
    - Summarize the key weather information clearly
    - Include relevant details like temperature, conditions, humidity, wind
    - Add helpful suggestions based on the weather (umbrella, sunscreen, etc.)
    - Use emojis to make responses more engaging (☀️ 🌧️ ❄️ 🌤️ etc.)

    EXAMPLE INTERACTIONS:
    User: "What's the weather in Paris?"
    You: "Let me check the current weather in Paris for you! 🌍"
    [Call get_current_weather with q="Paris,FR", units="metric", appid="{weather_api_key}"]
    Then provide a friendly summary of the results.

    User: "Will it rain in London tomorrow?"
    You: "I'll check the forecast for London! 🌧️"
    [Call get_weather_forecast with q="London,UK", units="metric", appid="{weather_api_key}"]
    Then analyze the forecast data and answer about rain probability.

    HANDLING ERRORS:
    - If a city is not found, suggest checking the spelling or adding country code
    - If the API returns an error, explain it in user-friendly terms
    - Always be helpful and suggest alternatives

    Remember: You're here to help people plan their day and activities based on weather!
    """,

    tools=[weather_toolset]
)

# For backwards compatibility and easier imports
root_agent = weather_agent
