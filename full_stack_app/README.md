# Weather Assistant - Full Stack Application

A production-ready weather assistant powered by Google ADK and FastAPI with a custom React frontend.

## Architecture

### Backend (FastAPI + Google ADK)
- **Framework**: FastAPI with production best practices
- **AI Agent**: Google ADK with Gemini 2.0 Flash
- **Weather API**: OpenWeatherMap integration via OpenAPI toolset
- **Features**:
  - Structured logging with request tracing
  - Optional API key authentication
  - CORS configuration
  - Request timeout handling (30s default)
  - Input validation
  - Health checks with metrics
  - Error tracking

### Frontend (Next.js + React)
- **Framework**: Next.js 14 with TypeScript
- **UI**: Custom chat interface with Tailwind CSS
- **Icons**: Lucide React
- **Features**:
  - Real-time chat interface
  - Auto-scroll to latest messages
  - Loading states
  - Error handling
  - Token count display

## Setup

### Prerequisites
- Python 3.13+
- Node.js 18+
- OpenWeather API key (free at https://openweathermap.org/api)
- Google AI API key

### Backend Setup

1. Navigate to backend directory:
```bash
cd full_stack_app/backend
```

2. Create `.env` file:
```bash
# Required
GOOGLE_API_KEY=your_google_api_key
OPENWEATHER_API_KEY=your_openweather_api_key

# Optional
ENVIRONMENT=development
PORT=8000
ENABLE_AUTH=false
API_KEY=your_secret_key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
REQUEST_TIMEOUT=30
MAX_QUERY_LENGTH=10000
MAX_TOKENS=4096
GOOGLE_GENAI_USE_VERTEXAI=false
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python3 main.py
```

Server will start at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd full_stack_app/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

Frontend will start at `http://localhost:3000`

## API Endpoints

### Backend (FastAPI)

#### `GET /`
Root endpoint with API information

#### `GET /health`
Comprehensive health check with metrics
```json
{
  "status": "healthy",
  "service": "weather-assistant-api",
  "uptime_seconds": 123.45,
  "request_count": 10,
  "error_count": 0,
  "agent": {
    "name": "weather_assistant",
    "model": "gemini-2.0-flash"
  },
  "metrics": {
    "successful_requests": 10,
    "timeout_count": 0,
    "error_rate": 0.0
  }
}
```

#### `POST /invoke`
Invoke the weather assistant agent

**Request:**
```json
{
  "query": "What's the weather in Paris?",
  "temperature": 0.7,
  "max_tokens": 2048
}
```

**Response:**
```json
{
  "response": "Let me check the current weather in Paris for you! 🌍\n\nThe current weather in Paris, France is:\n- Temperature: 15°C\n- Conditions: Partly cloudy\n- Humidity: 65%\n- Wind: 12 km/h",
  "model": "gemini-2.0-flash",
  "tokens": 45,
  "request_id": "a31c2369-80ae-426d-99a8-50dcfb8bb5fe"
}
```

#### `GET /docs`
Interactive API documentation (Swagger UI)

## Testing

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Invoke agent
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the weather in Paris?",
    "temperature": 0.7,
    "max_tokens": 2048
  }'
```

### Using the Frontend

1. Start both backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Type a weather query like "What's the weather in London?"
4. Press Enter or click Send

## Configuration

### Backend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Environment (development/production) |
| `PORT` | `8000` | Server port |
| `ENABLE_AUTH` | `false` | Enable API key authentication |
| `API_KEY` | `None` | API key for authentication |
| `ALLOWED_ORIGINS` | `http://localhost:3000,http://localhost:5173` | CORS allowed origins |
| `REQUEST_TIMEOUT` | `30` | Request timeout in seconds |
| `MAX_QUERY_LENGTH` | `10000` | Maximum query length |
| `MAX_TOKENS` | `4096` | Maximum tokens in response |
| `GOOGLE_GENAI_USE_VERTEXAI` | `false` | Use Vertex AI instead of Gemini API |

## Production Deployment

### Backend

1. Set `ENVIRONMENT=production` in `.env`
2. Set `ENABLE_AUTH=true` and configure `API_KEY`
3. Configure specific `ALLOWED_ORIGINS` (no wildcards)
4. Use a production WSGI server like Gunicorn:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend

1. Update the API URL in `page.tsx` to your production backend URL
2. Build for production:

```bash
npm run build
npm start
```

## Features

### Weather Assistant Capabilities
- Get current weather for any city
- Get 5-day weather forecast
- Support multiple units (metric, imperial, standard)
- Detailed weather information (temperature, humidity, wind, etc.)
- Conversational and friendly responses

### Production Features
- Request tracing with unique IDs
- Comprehensive error handling
- Input validation
- Rate limiting ready
- Health monitoring
- Metrics tracking
- Structured logging

## Troubleshooting

### Backend Issues

**Error: "OPENWEATHER_API_KEY not found"**
- Add `OPENWEATHER_API_KEY` to your `.env` file

**Error: "GOOGLE_API_KEY not set"**
- Add `GOOGLE_API_KEY` to your `.env` file

**CORS errors**
- Check `ALLOWED_ORIGINS` includes your frontend URL
- Ensure both servers are running

### Frontend Issues

**Connection refused**
- Ensure backend is running on `http://localhost:8000`
- Check browser console for errors

**No response from agent**
- Check backend logs for errors
- Verify API keys are configured correctly

## License

MIT
