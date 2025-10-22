# Weather Assistant Backend

FastAPI server that exposes a Google ADK weather agent through REST API endpoints.

## Features

- 🌤️ Current weather information for any location
- 📅 5-day weather forecasts
- 🌍 Support for cities worldwide
- 🔄 RESTful API with CORS support
- 📚 Auto-generated API documentation

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Get OpenWeatherMap API Key

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from the dashboard

### 3. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
OPENWEATHER_API_KEY=your_actual_api_key_here
```

### 4. Run the Server

```bash
# Option 1: Using uvicorn directly
uvicorn main:app --reload

# Option 2: Using Python
python main.py
```

The server will start at: `http://localhost:8000`

## API Endpoints

### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "agent": "weather_assistant_ready",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Chat with Agent
```bash
POST /chat
Content-Type: application/json

{
  "message": "What's the weather in Paris?",
  "conversation_id": "optional-uuid"
}
```

Response:
```json
{
  "response": "The current weather in Paris is sunny with 22°C...",
  "conversation_id": "uuid-here",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Testing

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Chat request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather in London?"}'
```

### Using the Interactive API Docs

Visit `http://localhost:8000/docs` for Swagger UI documentation where you can test all endpoints interactively.

## Agent Capabilities

The weather agent can:
- Get current weather for any city
- Provide 5-day forecasts
- Support multiple units (metric, imperial)
- Give weather advice and suggestions
- Handle natural language queries

## Example Queries

- "What's the weather in Paris?"
- "Will it rain in London tomorrow?"
- "Show me the forecast for New York"
- "What's the temperature in Tokyo?"
- "Is it cold in Moscow right now?"

## Project Structure

```
backend/
├── agent.py              # Google ADK agent definition
├── main.py              # FastAPI server
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
├── .env                # Your actual credentials (gitignored)
└── README.md           # This file
```

## Troubleshooting

### API Key Issues
- Make sure your `.env` file exists and contains the API key
- Verify the API key is valid at OpenWeatherMap
- Check that the key is activated (can take a few minutes)

### CORS Errors
- Ensure the frontend URL is in the `allow_origins` list in `main.py`
- Default allows `http://localhost:3000` for Next.js

### Agent Not Responding
- Check the console logs for error messages
- Verify Google ADK is installed correctly
- Ensure all dependencies are installed

## Development

### Adding New Features

1. Modify `agent.py` to add new capabilities
2. Update the OpenAPI spec if adding new endpoints
3. Test with the `/docs` interface
4. Update this README

### Environment Variables

- `OPENWEATHER_API_KEY`: Required for weather data
- `GOOGLE_API_KEY`: Optional, for Google ADK features

## License

MIT
