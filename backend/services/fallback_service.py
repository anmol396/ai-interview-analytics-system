import logging

logger = logging.getLogger("fallback_service")

def get_internal_fallback_response(query: str, error_context: str = "") -> str:
    logger.info("Calling Internal Fallback System...")
    base_msg = "I'm currently operating in offline fallback mode. I've received your query but cannot provide an AI-generated analysis at the moment."
    
    if error_context:
        logger.info(f"Fallback context: {error_context}")
        
    return base_msg + "\n\nPlease try again later."
