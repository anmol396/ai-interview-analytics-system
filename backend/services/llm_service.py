import warnings
from backend.services.ai_router import get_ai_response, ask_llm

warnings.warn("llm_service.py is deprecated. Please use ai_router.py and the new modular service files.", DeprecationWarning, stacklevel=2)
