import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("gemini_service")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"

# ── New SDK: google-genai (replaces deprecated google-generativeai) ──
_client = None

def _get_client():
    """Lazy-initialize the Gemini client."""
    global _client
    if _client is None and GOOGLE_API_KEY:
        from google import genai
        _client = genai.Client(api_key=GOOGLE_API_KEY)
    return _client

_gemini_healthy = None

def test_gemini() -> bool:
    global _gemini_healthy
    if _gemini_healthy is not None:
        return _gemini_healthy
        
    if not GOOGLE_API_KEY or "your_google_api_key_here" in GOOGLE_API_KEY:
        logger.error("Gemini Error: API key not found in environment")
        _gemini_healthy = False
        return False
        
    try:
        logger.info("Calling Gemini API... (health check)")
        client = _get_client()
        if not client:
            raise Exception("Failed to create Gemini client")
        response = client.models.generate_content(
            model=DEFAULT_GEMINI_MODEL,
            contents="hello"
        )
        _gemini_healthy = True
        return True
    except Exception as e:
        logger.error(f"Gemini Error during health check: {str(e)}")
        _gemini_healthy = False
        return False

def ask_gemini(prompt: str, timeout: int = 10) -> str:
    logger.info("Calling Gemini API...")
    try:
        client = _get_client()
        if not client:
            raise Exception("Gemini client not initialized — missing API key?")
        response = client.models.generate_content(
            model=DEFAULT_GEMINI_MODEL,
            contents=prompt,
            config={"http_options": {"timeout": timeout * 1000}}  # timeout in ms
        )
        if not response or not hasattr(response, 'text'):
            raise Exception("Empty response from Gemini")
        logger.info("Gemini Response Summary: successfully received content")
        return response.text
    except Exception as e:
        logger.error(f"Gemini Error: {str(e)}")
        raise e
