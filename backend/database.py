import os
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# ─── Database URL Configuration ───────────────────────────────────────────────
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
print("USING DB:", DATABASE_URL)

# Track which DB engine is active
_active_db_type = "mysql"

def _build_mysql_engine(db_url: str):
    """Build a MySQL engine."""
    connect_args = {}

    if "freesqldatabase" in db_url:
        connect_args["ssl_disabled"] = True

    return create_engine(
        db_url,
        pool_pre_ping=True,       # Auto-reconnect stale connections
        pool_recycle=1800,         # Recycle connections every 30 min
        pool_size=3,              # Smaller pool for free-tier DBs
        max_overflow=5,
        connect_args=connect_args,
        echo=False,               # Set to True for SQL query logging
    )


def _try_connect_with_retry(engine, max_retries: int = 3, base_delay: float = 1.0):
    """Attempt to connect to the database with exponential backoff retry logic."""
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            delay = base_delay * (2 ** (attempt - 1))  # Exponential backoff: 1s, 2s, 4s
            logger.warning(
                f"⚠️  DB connection attempt {attempt}/{max_retries} failed: {e}"
            )
            if attempt < max_retries:
                logger.info(f"   Retrying in {delay:.1f}s...")
                time.sleep(delay)
    return False


def _initialize_engine():
    """Initialize the database engine strictly using MySQL."""
    if not SQLALCHEMY_DATABASE_URL:
        raise RuntimeError("DATABASE_URL not set in environment variables.")

    # Mask password in logs for security
    if "@" in SQLALCHEMY_DATABASE_URL:
        parts = SQLALCHEMY_DATABASE_URL.split("@")
        masked = parts[0].rsplit(":", 1)[0] + ":****@" + parts[1]
    else:
        masked = "configured"
    logger.info(f"🔌 Attempting MySQL connection: {masked}")

    mysql_engine = _build_mysql_engine(SQLALCHEMY_DATABASE_URL)
    if _try_connect_with_retry(mysql_engine, max_retries=3, base_delay=1.0):
        logger.info("Connected to MySQL")
        print("Connected to MySQL")
        return mysql_engine
    else:
        logger.error("❌ MySQL connection failed after 3 retries.")
        raise RuntimeError("MySQL database connection failed. Please ensure the DATABASE_URL is correct.")


# ─── Initialize Engine, Session, Base ──────────────────────────────────────────
engine = _initialize_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_active_db_type() -> str:
    """Return which database engine is active."""
    return _active_db_type


def test_db_connection() -> dict:
    """Test current database connection and return detailed health info."""
    result = {
        "connected": False,
        "db_type": _active_db_type,
        "latency_ms": None,
        "error": None,
    }
    try:
        start = time.time()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        latency = (time.time() - start) * 1000
        result["connected"] = True
        result["latency_ms"] = round(latency, 2)
        logger.info(f"✅ DB health check passed ({latency:.1f}ms)")
    except Exception as e:
        result["error"] = str(e)
        logger.error(f"❌ DB health check failed: {e}")
    return result


def reconnect_mysql() -> bool:
    """Attempt to reconnect to the MySQL database.
    Returns True if successful and engine was swapped."""
    global engine, SessionLocal

    if not SQLALCHEMY_DATABASE_URL:
        logger.error("Cannot reconnect: DATABASE_URL not set")
        return False

    try:
        new_engine = _build_mysql_engine(SQLALCHEMY_DATABASE_URL)
        if _try_connect_with_retry(new_engine, max_retries=2, base_delay=1.0):
            engine = new_engine
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            # Recreate tables on the new engine
            Base.metadata.create_all(bind=engine)
            logger.info("Connected to MySQL (reconnected)")
            return True
    except Exception as e:
        logger.error(f"❌ MySQL reconnect failed: {e}")
    return False
