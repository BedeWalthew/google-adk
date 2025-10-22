"""
Enterprise Multi-Agent Architecture Example

This demonstrates how to manage multiple agents at scale with:
- Single unified endpoint with agent selection
- Agent registry pattern
- Dynamic agent loading
- Per-agent metrics and monitoring
- Centralized configuration
"""

import asyncio
import logging
import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import your agents
from agent import weather_agent
from github_agent import root_agent as github_agent
# from other_agents import customer_support_agent, sales_agent, analytics_agent

load_dotenv()

# ============================================================================
# AGENT REGISTRY PATTERN
# ============================================================================

class AgentRegistry:
    """
    Central registry for all agents in the system.
    Provides discovery, routing, and lifecycle management.
    """
    
    def __init__(self):
        self._agents: Dict[str, Any] = {}
        self._runners: Dict[str, Runner] = {}
        self._metrics: Dict[str, Dict[str, int]] = {}
        self.session_service = InMemorySessionService()
    
    def register_agent(self, agent_id: str, agent: Any, description: str = ""):
        """Register an agent in the system."""
        self._agents[agent_id] = {
            "agent": agent,
            "description": description,
            "name": agent.name,
            "model": agent.model
        }
        
        # Create runner for this agent
        self._runners[agent_id] = Runner(
            app_name=f"{agent_id}_app",
            agent=agent,
            session_service=self.session_service
        )
        
        # Initialize metrics
        self._metrics[agent_id] = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens": 0
        }
        
        logger.info(f"✅ Registered agent: {agent_id} ({agent.name})")
    
    def get_agent(self, agent_id: str) -> Optional[Any]:
        """Get agent by ID."""
        return self._agents.get(agent_id, {}).get("agent")
    
    def get_runner(self, agent_id: str) -> Optional[Runner]:
        """Get runner for agent."""
        return self._runners.get(agent_id)
    
    def list_agents(self) -> Dict[str, Dict[str, Any]]:
        """List all registered agents."""
        return {
            agent_id: {
                "name": info["name"],
                "model": info["model"],
                "description": info["description"],
                "metrics": self._metrics.get(agent_id, {})
            }
            for agent_id, info in self._agents.items()
        }
    
    def update_metrics(self, agent_id: str, success: bool, tokens: int = 0):
        """Update metrics for an agent."""
        if agent_id in self._metrics:
            self._metrics[agent_id]["total_requests"] += 1
            if success:
                self._metrics[agent_id]["successful_requests"] += 1
                self._metrics[agent_id]["total_tokens"] += tokens
            else:
                self._metrics[agent_id]["failed_requests"] += 1
    
    def get_metrics(self, agent_id: str) -> Dict[str, int]:
        """Get metrics for a specific agent."""
        return self._metrics.get(agent_id, {})


# Global agent registry
agent_registry = AgentRegistry()

# ============================================================================
# CONFIGURATION
# ============================================================================

class Settings(BaseSettings):
    """Application configuration."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    
    app_name: str = "Enterprise Multi-Agent API"
    app_version: str = "1.0"
    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Security
    api_key: Optional[str] = None
    enable_auth: bool = False
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Agent settings
    request_timeout: int = 30
    max_query_length: int = 10000
    max_tokens: int = 4096
    
    def get_allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

settings = Settings()

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# LIFESPAN - REGISTER ALL AGENTS
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: register agents on startup."""
    logger.info("🚀 Enterprise Multi-Agent API starting up...")
    
    # Register all your agents here
    agent_registry.register_agent(
        agent_id="weather",
        agent=weather_agent,
        description="Provides current weather and forecasts for any location worldwide"
    )
    
    agent_registry.register_agent(
        agent_id="github",
        agent=github_agent,
        description="GitHub code review assistant that analyzes pull requests and provides feedback"
    )
    
    # Example: Register more agents
    # agent_registry.register_agent(
    #     agent_id="customer_support",
    #     agent=customer_support_agent,
    #     description="Handles customer inquiries and support tickets"
    # )
    # 
    # agent_registry.register_agent(
    #     agent_id="sales",
    #     agent=sales_agent,
    #     description="Assists with product information and sales inquiries"
    # )
    # 
    # agent_registry.register_agent(
    #     agent_id="analytics",
    #     agent=analytics_agent,
    #     description="Provides business analytics and data insights"
    # )
    
    logger.info(f"📊 Registered {len(agent_registry.list_agents())} agents")
    
    yield
    
    logger.info("🛑 Enterprise Multi-Agent API shutting down...")

# ============================================================================
# APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise-scale multi-agent API with centralized routing and management",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class AgentInvokeRequest(BaseModel):
    """Request model for agent invocation."""
    agent_id: str = Field(..., description="ID of the agent to invoke (e.g., 'weather', 'support')")
    query: str = Field(..., min_length=1, max_length=10000, description="Query for the agent")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Temperature for generation")
    max_tokens: int = Field(2048, ge=1, le=4096, description="Max tokens in response")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation continuity")

class AgentInvokeResponse(BaseModel):
    """Response model for agent invocation."""
    agent_id: str = Field(..., description="ID of the agent that processed the request")
    response: str = Field(..., description="Agent response text")
    model: str = Field(..., description="Model used")
    tokens: int = Field(..., description="Token count estimate")
    request_id: str = Field(..., description="Request tracking ID")
    session_id: str = Field(..., description="Session ID for conversation continuity")

class AgentInfo(BaseModel):
    """Information about an agent."""
    agent_id: str
    name: str
    model: str
    description: str
    metrics: Dict[str, int]

class AgentListResponse(BaseModel):
    """Response model for listing agents."""
    agents: Dict[str, AgentInfo]
    total_agents: int

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
        "total_agents": len(agent_registry.list_agents()),
        "endpoints": {
            "agents": "/agents (GET) - List all available agents",
            "invoke": "/invoke (POST) - Invoke any agent",
            "agent_metrics": "/agents/{agent_id}/metrics (GET) - Get agent metrics",
            "health": "/health (GET) - Health check",
            "docs": "/docs - API documentation"
        }
    }

@app.get("/agents", response_model=AgentListResponse)
async def list_agents():
    """
    List all available agents in the system.
    
    Returns information about each agent including:
    - Agent ID and name
    - Model being used
    - Description of capabilities
    - Usage metrics
    """
    agents_info = agent_registry.list_agents()
    
    agents_dict = {
        agent_id: AgentInfo(
            agent_id=agent_id,
            name=info["name"],
            model=info["model"],
            description=info["description"],
            metrics=info["metrics"]
        )
        for agent_id, info in agents_info.items()
    }
    
    return AgentListResponse(
        agents=agents_dict,
        total_agents=len(agents_dict)
    )

@app.get("/agents/{agent_id}/metrics")
async def get_agent_metrics(agent_id: str):
    """Get detailed metrics for a specific agent."""
    if not agent_registry.get_agent(agent_id):
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_id}' not found"
        )
    
    metrics = agent_registry.get_metrics(agent_id)
    agent_info = agent_registry.list_agents()[agent_id]
    
    return {
        "agent_id": agent_id,
        "agent_name": agent_info["name"],
        "metrics": metrics,
        "success_rate": (
            metrics["successful_requests"] / max(metrics["total_requests"], 1)
        ) if metrics["total_requests"] > 0 else 0,
        "avg_tokens_per_request": (
            metrics["total_tokens"] / max(metrics["successful_requests"], 1)
        ) if metrics["successful_requests"] > 0 else 0
    }

@app.post("/invoke", response_model=AgentInvokeResponse)
async def invoke_agent(request: AgentInvokeRequest):
    """
    Invoke any registered agent with a query.
    
    This is the main endpoint for interacting with agents.
    Specify the agent_id to route to the appropriate agent.
    
    Example:
    ```json
    {
        "agent_id": "weather",
        "query": "What's the weather in Paris?",
        "temperature": 0.7,
        "max_tokens": 2048
    }
    ```
    """
    request_id = str(uuid.uuid4())
    
    logger.info(
        f"invoke_agent.start - request_id={request_id} "
        f"agent_id={request.agent_id} query_len={len(request.query)}"
    )
    
    try:
        # Get agent and runner
        agent = agent_registry.get_agent(request.agent_id)
        runner = agent_registry.get_runner(request.agent_id)
        
        if not agent or not runner:
            raise HTTPException(
                status_code=404,
                detail=f"Agent '{request.agent_id}' not found. "
                       f"Available agents: {list(agent_registry.list_agents().keys())}"
            )
        
        # Validate query length
        if len(request.query) > settings.max_query_length:
            raise HTTPException(
                status_code=400,
                detail=f"Query exceeds maximum length of {settings.max_query_length}"
            )
        
        # Create or get session
        if request.session_id:
            # Use existing session
            session_id = request.session_id
        else:
            # Create new session
            session = await agent_registry.session_service.create_session(
                app_name=f"{request.agent_id}_app",
                user_id="api_user"
            )
            session_id = session.id
        
        # Update agent config
        agent.generate_content_config = types.GenerateContentConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens
        )
        
        # Create message
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
                    session_id=session_id,
                    new_message=new_message
                ):
                    if event.content and event.content.parts:
                        text = event.content.parts[0].text
                        if text:
                            response_text += text
        except asyncio.TimeoutError:
            agent_registry.update_metrics(request.agent_id, success=False)
            raise HTTPException(
                status_code=504,
                detail=f"Request exceeded {settings.request_timeout} second timeout"
            )
        
        # Calculate tokens
        token_count = len(response_text.split())
        
        # Update metrics
        agent_registry.update_metrics(request.agent_id, success=True, tokens=token_count)
        
        logger.info(
            f"invoke_agent.success - request_id={request_id} "
            f"agent_id={request.agent_id} tokens={token_count}"
        )
        
        return AgentInvokeResponse(
            agent_id=request.agent_id,
            response=response_text,
            model=agent.model,
            tokens=token_count,
            request_id=request_id,
            session_id=session_id
        )
        
    except HTTPException:
        raise
    
    except Exception as e:
        agent_registry.update_metrics(request.agent_id, success=False)
        logger.error(
            f"invoke_agent.error - request_id={request_id} "
            f"agent_id={request.agent_id} error={str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )

@app.get("/health")
async def health_check():
    """Health check with system-wide metrics."""
    agents = agent_registry.list_agents()
    
    total_requests = sum(
        agent["metrics"]["total_requests"] 
        for agent in agents.values()
    )
    total_successful = sum(
        agent["metrics"]["successful_requests"] 
        for agent in agents.values()
    )
    
    return {
        "status": "healthy",
        "service": "enterprise-multi-agent-api",
        "environment": settings.environment,
        "total_agents": len(agents),
        "system_metrics": {
            "total_requests": total_requests,
            "successful_requests": total_successful,
            "success_rate": total_successful / max(total_requests, 1) if total_requests > 0 else 0
        },
        "agents": list(agents.keys())
    }

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
