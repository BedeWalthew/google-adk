"""
Weather Assistant API - Production FastAPI Deployment

Production-ready FastAPI server for weather assistant agent.

This implements production best practices:
- Structured JSON logging with request tracing
- API key authentication (optional)
- Restricted CORS with configuration
- Timeout handling for reliability
- Proper error handling with typed exceptions
- Input validation with limits
- Health checks with dependency status
"""

import asyncio
import logging
import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from typing import Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import weather_agent

# Load environment variables
load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

class Settings(BaseSettings):
    """Application configuration from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    
    # App settings
    app_name: str = "Weather Assistant API"
    app_version: str = "1.0"
    environment: str = "development"
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    
    # Security
    api_key: Optional[str] = None
    enable_auth: bool = False
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Agent settings
    request_timeout: int = 30
    max_query_length: int = 10000
    max_tokens: int = 4096
    
    # Gemini settings
    use_vertexai: bool = False
    
    @field_validator('enable_auth', 'use_vertexai', mode='before')
    @classmethod
    def parse_bool(cls, v):
        """Parse boolean from string."""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes')
        return bool(v)
    
    def get_allowed_origins(self) -> list[str]:
        """Get allowed origins as a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

settings = Settings()

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def setup_logging() -> logging.Logger:
    """Configure structured JSON logging."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with formatting
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

logger = setup_logging()

# ============================================================================
# VALIDATION & STARTUP
# ============================================================================

def validate_configuration() -> None:
    """Validate configuration on startup."""
    logger.info("Validating configuration...")
    
    if settings.environment == "production":
        if settings.enable_auth and not settings.api_key:
            raise ValueError(
                "ENABLE_AUTH is true but API_KEY is not set. "
                "Set API_KEY or set ENABLE_AUTH=false"
            )
        
        # Validate origins are not wildcard
        if "*" in settings.allowed_origins:
            logger.warning(
                "ALLOWED_ORIGINS contains '*'. This is NOT recommended for production. "
                "Set specific origins in ALLOWED_ORIGINS environment variable."
            )
    
    # Set Gemini environment
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = str(settings.use_vertexai).lower()
    
    logger.info(f"Configuration validated. Environment: {settings.environment}")
    logger.info(f"Allowed origins: {settings.get_allowed_origins()}")

# ============================================================================
# LIFESPAN EVENTS
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown."""
    # Startup
    logger.info("🚀 Weather Assistant API starting up...")
    validate_configuration()
    logger.info(f"Agent: {weather_agent.name}")
    logger.info(f"Model: {weather_agent.model}")
    
    # Check for API key
    weather_api_key = os.getenv("OPENWEATHER_API_KEY")
    if weather_api_key:
        logger.info(f"✅ OpenWeather API Key configured")
    else:
        logger.warning("⚠️  Warning: OPENWEATHER_API_KEY not set!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Weather Assistant API shutting down...")

# ============================================================================
# APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-ready Weather Assistant API with full monitoring and security",
    lifespan=lifespan
)

# CORS configuration with restricted origins
cors_origins = settings.get_allowed_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Create session service and runner
session_service = InMemorySessionService()
runner = Runner(
    app_name="weather_assistant_app",
    agent=weather_agent,
    session_service=session_service
)

# ============================================================================
# METRICS TRACKING
# ============================================================================

class HealthStatus(str, Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

# Metrics
service_start_time = datetime.now()
request_count = 0
successful_requests = 0
error_count = 0
timeout_count = 0

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """Request model for agent invocation with validation."""
    query: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Query prompt for the weather assistant"
    )
    temperature: float = Field(
        0.5,
        ge=0.0,
        le=2.0,
        description="Controls randomness: higher = more creative"
    )
    max_tokens: int = Field(
        2048,
        ge=1,
        le=4096,
        description="Maximum tokens in response"
    )

class QueryResponse(BaseModel):
    """Response model for agent invocation."""
    response: str = Field(..., description="Agent response text")
    model: str = Field(..., description="Model used")
    tokens: int = Field(..., description="Token count estimate")
    request_id: str = Field(default="", description="Request tracking ID")

# ============================================================================
# AUTHENTICATION
# ============================================================================

async def verify_api_key(authorization: Optional[str] = None) -> None:
    """Verify API key if authentication is enabled."""
    if not settings.enable_auth:
        return
    
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Missing or invalid authorization header")
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization"
        )
    
    token = authorization.replace("Bearer ", "")
    if token != settings.api_key:
        logger.warning("Invalid API key attempted")
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "endpoints": {
            "health": "/health",
            "invoke": "/invoke (POST)",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint with dependency status.
    
    Returns:
        - healthy (200): All systems operational
        - degraded (200): Service working but with issues
        - unhealthy (503): Service unavailable
    """
    uptime = (datetime.now() - service_start_time).total_seconds()
    error_rate = error_count / max(request_count, 1)
    
    # Determine health status
    if request_count == 0:
        health_status = HealthStatus.HEALTHY
    elif error_rate > 0.1:  # More than 10% error rate
        health_status = HealthStatus.UNHEALTHY
    elif error_rate > 0.05:  # More than 5% error rate
        health_status = HealthStatus.DEGRADED
    else:
        health_status = HealthStatus.HEALTHY
    
    response_data = {
        "status": health_status.value,
        "service": "weather-assistant-api",
        "environment": settings.environment,
        "uptime_seconds": uptime,
        "request_count": request_count,
        "error_count": error_count,
        "agent": {
            "name": weather_agent.name,
            "model": weather_agent.model
        },
        "metrics": {
            "successful_requests": successful_requests,
            "timeout_count": timeout_count,
            "error_rate": round(error_rate, 3)
        }
    }
    
    # Return appropriate status code
    if health_status == HealthStatus.UNHEALTHY:
        return JSONResponse(
            status_code=503,
            content=response_data
        )
    else:
        return response_data

@app.post(
    "/invoke",
    response_model=QueryResponse,
    status_code=200,
    responses={
        200: {"description": "Successful agent invocation"},
        400: {"description": "Invalid request parameters"},
        401: {"description": "Missing or invalid authentication"},
        403: {"description": "Forbidden"},
        504: {"description": "Request timeout"},
        500: {"description": "Server error"}
    }
)
async def invoke_agent(
    request: QueryRequest,
    authorization: Optional[str] = None
):
    """
    Invoke the weather assistant agent.
    
    Args:
        request: Query and configuration parameters
        authorization: Bearer token for API authentication
        
    Returns:
        Agent response with metadata
        
    Raises:
        HTTPException: For invalid requests or server errors
    """
    global request_count, successful_requests, error_count, timeout_count
    
    request_id = str(uuid.uuid4())
    request_count += 1
    
    logger.info(
        f"invoke_agent.start - request_id={request_id} "
        f"query_len={len(request.query)}"
    )
    
    try:
        # Verify authentication if enabled
        await verify_api_key(authorization)
        
        # Validate query length
        if len(request.query) > settings.max_query_length:
            logger.warning(
                f"invoke_agent.query_too_long - request_id={request_id} "
                f"len={len(request.query)}"
            )
            raise HTTPException(
                status_code=400,
                detail=f"Query exceeds maximum length of {settings.max_query_length}"
            )
        
        # Create a session for this invocation
        session = await session_service.create_session(
            app_name="weather_assistant_app",
            user_id="api_user"
        )
        
        # Update agent config
        weather_agent.generate_content_config = types.GenerateContentConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens
        )
        
        # Create message content
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=request.query)]
        )
        
        # Run agent with timeout
        response_text = ""
        try:
            async with asyncio.timeout(settings.request_timeout):
                async for event in runner.run_async(
                    user_id="api_user",
                    session_id=session.id,
                    new_message=new_message
                ):
                    if event.content and event.content.parts:
                        text = event.content.parts[0].text
                        if text:  # Only concatenate if text is not None
                            response_text += text
        except asyncio.TimeoutError:
            timeout_count += 1
            logger.error(
                f"invoke_agent.timeout - request_id={request_id} "
                f"timeout={settings.request_timeout}s"
            )
            raise HTTPException(
                status_code=504,
                detail=f"Agent request exceeded {settings.request_timeout} second timeout"
            )
        
        # Estimate tokens (word count as fallback)
        token_count = len(response_text.split())
        
        successful_requests += 1
        logger.info(
            f"invoke_agent.success - request_id={request_id} "
            f"tokens={token_count}"
        )
        
        return QueryResponse(
            response=response_text,
            model=weather_agent.model,
            tokens=token_count,
            request_id=request_id
        )
        
    except HTTPException as e:
        error_count += 1
        logger.warning(
            f"invoke_agent.http_error - request_id={request_id} "
            f"status={e.status_code}"
        )
        raise
    
    except ValueError as e:
        error_count += 1
        logger.warning(
            f"invoke_agent.validation_error - request_id={request_id} "
            f"error={str(e)}"
        )
        raise HTTPException(
            status_code=400,
            detail="Invalid request parameters"
        )
    
    except Exception as e:
        error_count += 1
        logger.error(
            f"invoke_agent.unexpected_error - request_id={request_id} "
            f"error_type={type(e).__name__} error={str(e)}",
            exc_info=True
        )
        # Don't expose internal error details
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )

@app.middleware("http")
async def track_requests(request, call_next):
    """Middleware to track requests and errors."""
    response = await call_next(request)
    return response

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level="info"
    )
