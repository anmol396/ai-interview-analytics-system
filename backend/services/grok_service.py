import os
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("grok_service")

GROK_API_KEY = os.getenv("GROK_API_KEY")
DEFAULT_GROK_MODEL = "llama-3.1-8b-instant"

_client = None

def _get_client():
    global _client
    if _client is None and GROK_API_KEY:
        try:
            _client = Groq(api_key=GROK_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
    return _client

_grok_healthy = None

def test_grok() -> bool:
    """Tests Grok connectivity with caching."""
    global _grok_healthy
    if _grok_healthy is not None:
        return _grok_healthy
    if not GROK_API_KEY:
        logger.error("Grok Error: GROK_API_KEY not found in environment")
        return False

    client = _get_client()
    if not client: return False

    try:
        logger.info("Grok health check: sending test request...")
        # Use a very small request for health check
        client.chat.completions.create(
            model=DEFAULT_GROK_MODEL,
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5,
            timeout=5
        )
        _grok_healthy = True
        return True
    except Exception as e:
        logger.error(f"Grok health check FAILED: {str(e)}")
        _grok_healthy = False
        return False

def ask_grok(prompt: str, timeout: int = 10) -> str:
    """Calls Grok API using the official SDK."""
    logger.info("Calling Grok API...")
    client = _get_client()
    if not client:
        raise Exception("Groq client not initialized")
    
    try:
        response = client.chat.completions.create(
            model=DEFAULT_GROK_MODEL,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty content in Grok response")
        logger.info("Grok Response Summary: Successfully received completions.")
        return content
    except Exception as e:
        logger.error(f"Grok Error: {str(e)}")
        # Provide a more descriptive error if it's a known issue
        if "invalid_api_key" in str(e).lower():
            logger.error("Invalid Groq API key")
        elif "rate_limit" in str(e).lower():
            logger.error("Groq quota exceeded")
        raise e
