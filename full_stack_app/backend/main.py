"""
Weather Assistant API - Using AG-UI ADK
A FastAPI backend that integrates Google ADK weather agent with AG-UI ADK wrapper.
"""

import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# AG-UI ADK integration imports
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# Import the weather agent
from agent import weather_agent

# Load environment variables
load_dotenv()

# ============================================================================
# LOGGING SETUP
# ============================================================================

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# AGENT SETUP WITH AG-UI ADK
# ============================================================================

# Wrap ADK agent with AG-UI middleware
agent = ADKAgent(
    adk_agent=weather_agent,
    app_name="weather_assistant_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True,
)

# ============================================================================
# FASTAPI APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="Weather Assistant API",
    description="API for interacting with the Google ADK Weather Assistant using AG-UI ADK",
    version="1.0.0"
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# LOGGING MIDDLEWARE
# ============================================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and their payloads"""
    
    # Log request details
    print("\n" + "="*80)
    print(f"📥 INCOMING REQUEST - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print(f"Method: {request.method}")
    print(f"URL: {request.url.path}")
    print(f"Client: {request.client.host if request.client else 'Unknown'}")
    
    # Log headers (excluding sensitive ones)
    print("\n📋 Headers:")
    for header, value in request.headers.items():
        if header.lower() not in ['authorization', 'cookie']:
            print(f"  {header}: {value}")
    
    # Log request body for POST/PUT/PATCH
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.body()
            if body:
                try:
                    # Try to parse as JSON for pretty printing
                    json_body = json.loads(body)
                    print("\n📦 Request Payload (JSON):")
                    print(json.dumps(json_body, indent=2))
                except json.JSONDecodeError:
                    # If not JSON, print as string
                    print("\n📦 Request Payload (Raw):")
                    print(body.decode('utf-8', errors='replace')[:1000])  # Limit to 1000 chars
            
            # Important: Recreate the request with the body since we consumed it
            async def receive():
                return {"type": "http.request", "body": body}
            
            request._receive = receive
        except Exception as e:
            print(f"\n⚠️  Error reading request body: {e}")
    
    print("="*80 + "\n")
    
    # Process the request
    response = await call_next(request)
    
    # Log response
    print("\n" + "="*80)
    print(f"📤 RESPONSE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print(f"Status: {response.status_code}")
    print(f"Path: {request.url.path}")
    print("="*80 + "\n")
    
    return response

# ============================================================================
# ENDPOINTS
# ============================================================================

# Add ADK endpoint - this creates a /copilotkit endpoint
# This endpoint is designed to work with CopilotKit on the frontend
add_adk_fastapi_endpoint(app, agent, path="/copilotkit")

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Weather Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "copilotkit": "/copilotkit",
            "docs": "/docs"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to verify the service is running"""
    return {
        "status": "healthy",
        "agent": "weather_assistant_ready",
        "framework": "ag-ui-adk"
    }

# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("\n" + "="*60)
    print("🚀 Weather Assistant API Starting...")
    print("="*60)
    print(f"Agent: {weather_agent.name}")
    print(f"Model: {weather_agent.canonical_model}")
    
    # Check for API key
    weather_api_key = os.getenv("OPENWEATHER_API_KEY")
    if weather_api_key:
        print(f"✅ OpenWeather API Key: {weather_api_key[:8]}...")
    else:
        print("⚠️  Warning: OPENWEATHER_API_KEY not set!")
    
    print("="*60)
    print("📡 Server ready at: http://localhost:8000")
    print("📚 API Docs at: http://localhost:8000/docs")
    print("🔌 CopilotKit endpoint at: http://localhost:8000/copilotkit")
    print("="*60 + "\n")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("\n👋 Weather Assistant API shutting down...")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
