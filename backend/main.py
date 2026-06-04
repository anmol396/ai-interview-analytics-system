import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import Base, engine, test_db_connection, get_active_db_type, reconnect_mysql
from backend.routes import ai, candidate, dashboard, auth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    logger.info("🚀 Starting AI HR Analytics System...")
    
    # Log active DB type
    db_type = get_active_db_type()
    logger.info(f"📦 Active database: {db_type}")
    
    # Create tables if they don't exist
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables verified/created")
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
    
    # Log registered routes
    for route in app.routes:
        if hasattr(route, 'methods'):
            logger.info(f"  📌 {route.methods} {route.path}")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down AI HR Analytics System...")

app = FastAPI(title="AI HR Analytics System", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite defaults
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(candidate.router)
app.include_router(dashboard.router)
app.include_router(ai.router)

@app.get("/")
def read_root():
    db_type = get_active_db_type()
    return {
        "message": f"HR Analytics System API — Connected to {db_type.upper()}",
        "database": db_type,
    }

@app.get("/health")
def health_check():
    """Comprehensive health check endpoint that tests actual DB connectivity."""
    db_health = test_db_connection()
    return {
        "status": "healthy" if db_health["connected"] else "degraded",
        "database": {
            "type": db_health["db_type"],
            "connected": db_health["connected"],
            "latency_ms": db_health["latency_ms"],
            "error": db_health["error"],
        },
    }

@app.post("/reconnect-db")
def reconnect_database():
    """Attempt to reconnect to MySQL (useful after fixing credentials/IP whitelist)."""
    success = reconnect_mysql()
    return {
        "success": success,
        "active_db": get_active_db_type(),
        "message": (
            "Reconnected to MySQL successfully!"
            if success
            else "MySQL reconnection failed. Please check your credentials and network."
        ),
    }
