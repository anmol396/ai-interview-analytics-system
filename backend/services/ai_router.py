import logging
from backend.services.grok_service import test_grok, ask_grok
from backend.services.gemini_service import test_gemini, ask_gemini
from backend.services.fallback_service import get_internal_fallback_response

logger = logging.getLogger("ai_router")

def get_ai_response(query: str) -> str:
    """
    Central routing function for AI inferences.
    Priority fallback: Grok -> Gemini -> Internal Fallback
    """
    last_error = ""

    # 1. Try Grok
    if test_grok():
        try:
            return ask_grok(query, timeout=10)
        except Exception as e:
            last_error = f"Grok Error: {str(e)}"
            logger.error(last_error)
            # Switch to next priority automatically
    else:
        last_error = "Grok API is invalid or not responding"
        logger.warning(f"{last_error}, skipping to Gemini.")

    # 2. Try Gemini
    if test_gemini():
        try:
            return ask_gemini(query, timeout=10)
        except Exception as e:
            last_error = f"Gemini Error: {str(e)}"
            logger.error(last_error)
            # Switch to fallback
    else:
        last_error = "Gemini API is invalid or not responding"
        logger.warning(f"{last_error}, skipping to fallback.")
        
    # 3. Use internal fallback
    return get_internal_fallback_response(query, error_context=last_error)

# Backwards compatibility binding
ask_llm = get_ai_response
