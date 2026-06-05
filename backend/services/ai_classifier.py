"""
HR Query Classifier Module
Classifies natural language HR queries into structured intents for processing.
Supports 19 distinct intent types with confidence scoring and fuzzy matching.
"""

import re
import difflib
from typing import Dict, Tuple, Optional, Any, List


# ═════════════════════════════════════════════════════════════════════════════
# CONFIG SECTION
# ═════════════════════════════════════════════════════════════════════════════

# Known roles in the system
KNOWN_ROLES = ["ML Engineer", "Product Manager", "Data Analyst", "Backend Developer"]

# Role aliases and mappings (supports fuzzy matching)
ROLE_MAP = {
    "project manager": "product manager",
    "project mgr": "product manager",
    "pm": "product manager",
    "backend dev": "backend developer",
    "backend developer": "backend developer",
    "ml": "ml engineer",
    "machine learning": "ml engineer",
    "data analyst": "data analyst",
    "product manager": "product manager",
}

# Column name mappings
COLUMN_MAP = {
    "hr score": "hr_evaluation",
    "hr evaluation": "hr_evaluation",
    "technical score": "technical_assessment",
    "technical assessment": "technical_assessment",
    "written score": "written_test",
    "written test": "written_test",
    "pm score": "pm_assessment",
    "pm assessment": "pm_assessment",
    "total score": "total_score",
    "written": "written_test",
    "technical": "technical_assessment",
    "pm": "pm_assessment",
    "hr": "hr_evaluation"
}

# Out of scope keywords (defensive guard)
OUT_OF_SCOPE_KEYWORDS = [
    "prime minister", "weather", "elon musk", "president", 
    "news", "stock price", "capital of", "politics", "india", 
    "price of", "crypto", "bitcoin", "football", "cricket"
]

# Intent-specific trigger keywords
SUMMARY_KEYWORDS = ["summary", "overall performance", "stats", "statistics"]
RECOMMENDATION_KEYWORDS = ["recommend", "best candidate", "hire", "should we hire", "suggest", "best fit"]
COUNT_KEYWORDS = ["how many", "count", "number of"]
BEST_WORST_KEYWORDS = [
    "best round", "worst round", "lowest score", "highest score",
    "scored the less", "scored the most", "scored the least", "which round",
    "who scored highest", "who scored lowest", "scored the highest"
]
ANALYTICS_KEYWORDS = ["distribution", "by role", "role count", "role wise", "each role", "role-wise", "analytics", "dashboard", "statistics", "stats", "report"]
CONCEPTUAL_KEYWORDS = ["difference", "explain", "define", "why"]
GENERAL_KEYWORDS = ["what", "who", "explain", "difference", "define", "why", "how"]
HR_KEYWORDS = ["candidate", "score", "interview", "hiring", "talent", "employee"]

# Direction words for best/worst classification
DIRECTION_BEST = ["best", "most", "max", "highest", "maximum"]
DIRECTION_WORST = ["worst", "less", "least", "lowest", "minimal", "min", "minimum"]

# Status mapping
STATUS_KEYWORDS = {
    "pass": "passed",
    "passed": "passed",
    "fail": "failed",
    "failed": "failed",
    "pending": "pending"
}

# Name extraction triggers (sorted by length, descending)
NAME_TRIGGERS = [
    "tell me about", "profile of", "tell me", "role of", "details of",
    "who is", "about", "candidate", "identify", "find", "show me"
]

# Intent priority system (higher value = higher priority)
INTENT_PRIORITY = {
    "BEST_WORST_ROUND": 16,
    "SINGLE_METRIC": 15,
    "COMPARE": 14,
    "ROLE": 13,
    "COUNT": 12,
    "PERFORMANCE": 11,
    "GENERAL": 10,
}


# ═════════════════════════════════════════════════════════════════════════════
# COMPILED REGEX PATTERNS (for performance)
# ═════════════════════════════════════════════════════════════════════════════

REGEX_NUMBER = re.compile(r'\b(\d+)\b')
REGEX_PUNCTUATION = re.compile(r'[?.,!;:]')
REGEX_WHITESPACE = re.compile(r'\s+')
REGEX_COMPARE_TOP = re.compile(r'compare\s+top\s+(\d+)\s+(.+)', re.IGNORECASE)
REGEX_TOP_N = re.compile(r'top\s+(\d+)', re.IGNORECASE)
REGEX_BETWEEN = re.compile(r'between\s+(\d+)\s+and\s+(\d+)', re.IGNORECASE)
REGEX_MULTI_FILTER = re.compile(
    r'(\w+)\s*(>=|<=|>|<|=)\s*(\d+)\s+and\s+(\w+)\s*(>=|<=|>|<|=)\s*(\d+)',
    re.IGNORECASE
)
REGEX_NAME_EXTRACTION = re.compile(r'(?:round|for|about|of)\s+([a-z]+(?:\s+[a-z]+)+)', re.IGNORECASE)
REGEX_SPLIT_KEYWORDS = re.compile(r'\b(?:from|with|and|then|please|kindly|now|also)\b', re.IGNORECASE)


# ═════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def _clean_query(query: str) -> str:
    """
    Clean and normalize a query string.

    Args:
        query: Raw query string

    Returns:
        Cleaned, lowercase query with normalized whitespace
    """
    q = query.lower().strip()
    q = REGEX_PUNCTUATION.sub(' ', q).strip()
    q = REGEX_WHITESPACE.sub(' ', q)
    return q


def _extract_first_number(query: str) -> Optional[int]:
    """Extract the first number from a query string."""
    match = REGEX_NUMBER.search(query)
    return int(match.group(1)) if match else None


def _has_any_keyword(query: str, keywords: List[str]) -> bool:
    """Check if query contains any keyword from the list (substring match)."""
    return any(keyword in query for keyword in keywords)


def _has_any_keyword_boundary(query: str, keywords: List[str]) -> bool:
    """Check if query matches any keyword with word boundaries."""
    return any(re.search(rf'\b{re.escape(word)}\b', query) for word in keywords)


def _get_direction(query: str) -> str:
    """
    Determine if the query is asking for best or worst.

    Args:
        query: Cleaned query string

    Returns:
        "best", "worst", or "both"
    """
    has_best = _has_any_keyword(query, DIRECTION_BEST)
    has_worst = _has_any_keyword(query, DIRECTION_WORST)

    if has_best and has_worst:
        return "both"
    elif has_worst:
        return "worst"
    else:
        return "best"


def _extract_limit(query: str, default: int = 5) -> int:
    """
    Extract top N limit from query (e.g., "top 10" returns 10).

    Args:
        query: Cleaned query string
        default: Default limit if not found

    Returns:
        Extracted limit or default value
    """
    match = REGEX_TOP_N.search(query)
    return int(match.group(1)) if match else default


def _is_out_of_scope(query: str) -> bool:
    """Check if query is out of scope."""
    return _has_any_keyword_boundary(query, OUT_OF_SCOPE_KEYWORDS)


def _extract_potential_roles(query: str) -> List[str]:
    """
    Extract all potential role matches from query.

    Args:
        query: Cleaned query string

    Returns:
        List of matched role keys (longest first)
    """
    potential = list(ROLE_MAP.keys()) + [r.lower() for r in KNOWN_ROLES]
    potential = sorted(potential, key=len, reverse=True)

    found_roles = []
    for role_key in potential:
        if re.search(rf'\b{re.escape(role_key)}(?:s)?\b', query):
            found_roles.append(role_key)

    return found_roles


def _add_confidence(result: Dict[str, Any], confidence: float) -> Dict[str, Any]:
    """
    Add confidence score to result dictionary.

    Args:
        result: Result dictionary
        confidence: Confidence score (0.0 to 1.0)

    Returns:
        Updated result with confidence key
    """
    result["confidence"] = confidence
    return result


def _is_count_query(query: str) -> bool:
    """Check if query is asking for a count."""
    return _has_any_keyword(query, COUNT_KEYWORDS) or ("total" in query and "score" not in query)


def _extract_name_from_query(query: str, trigger: str) -> str:
    """
    Extract candidate name from query after a trigger phrase.

    Args:
        query: Cleaned query string
        trigger: Trigger phrase (e.g., "tell me about")

    Returns:
        Extracted name string
    """
    parts = re.split(rf'{re.escape(trigger)}', query, maxsplit=1)
    name_str = parts[-1].strip() if len(parts) > 1 else query.replace(trigger, '').strip()
    if trigger in ["role", "details", "tell me", "profile"]:
        name_str = re.sub(r'^(?:of|about)\s+', '', name_str).strip()
    return name_str


# ═════════════════════════════════════════════════════════════════════════════
# MAIN FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def get_closest_role(requested_role: str) -> Tuple[Optional[str], bool, Optional[str]]:
    """
    Find the closest matching role from KNOWN_ROLES.

    Supports three matching strategies:
    1. ROLE_MAP mapping (e.g., "pm" -> "product manager")
    2. Exact match in KNOWN_ROLES
    3. Fuzzy match using difflib (cutoff=0.5)

    Args:
        requested_role: User-provided role string

    Returns:
        Tuple of (normalized_role, is_exact_match, suggested_role)
    """
    requested_role = requested_role.lower().strip()

    # Check ROLE_MAP first
    if requested_role in ROLE_MAP:
        mapped = ROLE_MAP[requested_role].lower()
        for kr in KNOWN_ROLES:
            if kr.lower() == mapped:
                return kr, False, kr

    # Check exact match in KNOWN_ROLES
    for kr in KNOWN_ROLES:
        if kr.lower() == requested_role:
            return kr, True, None

    # Fuzzy match using difflib
    matches = difflib.get_close_matches(
        requested_role,
        [r.lower() for r in KNOWN_ROLES],
        n=1,
        cutoff=0.5
    )
    if matches:
        for kr in KNOWN_ROLES:
            if kr.lower() == matches[0]:
                return kr, False, kr

    return None, False, None

def classify_query(query: str) -> Dict[str, Any]:
    """
    Classify a user query into an intent type.

    This function analyzes natural language queries and categorizes them
    into specific intents that can be processed by backend handlers.

    Supported intents (priority order):
    - BEST_WORST_ROUND: Which round performed best/worst for a candidate
    - SINGLE_METRIC: Get specific metric for a candidate
    - COMPARE: Compare two candidates
    - ROLE: Get candidates by role
    - COUNT: Count candidates with filters
    - PERFORMANCE: Get top performers
    - GENERAL: General conceptual questions
    - RECOMMENDATION: Hiring recommendations
    - SUMMARY: Overall performance summary
    - ANALYTICS: Distribution by category
    - ROLE_ANALYTICS: Analytics by role
    - TOP_METRIC: Highest/lowest metric value
    - MULTI_FILTER: Multiple filter conditions
    - ROUND_FILTER: Filter by round metrics
    - FILTER: Simple score filtering
    - STATUS: Filter by status
    - NAME: Get candidate details
    - COMPARE_TOP: Compare top N from role
    - OUT_OF_SCOPE: Query outside HR domain

    Args:
        query: Natural language query string

    Returns:
        Dictionary with 'intent' key and additional context-specific keys
        Example: {"intent": "ROLE", "role": "ML Engineer", "confidence": 0.93}

    Examples:
        >>> classify_query("who scored highest in technical")
        {"intent": "TOP_METRIC", "metric": "technical", "direction": "best", "confidence": 0.88}

        >>> classify_query("out of 4 rounds in which round Brian Oliver scored the less")
        {"intent": "BEST_WORST_ROUND", "name": "Brian Oliver", "direction": "worst", "confidence": 0.88}

        >>> classify_query("compare top 5 ML engineers")
        {"intent": "COMPARE_TOP", "role": "ML Engineer", "limit": 5, "confidence": 0.87}
    """
    q = _clean_query(query)

    # ─────────────────────────────────────────────────────────────────────────
    # DEFENSIVE GUARD: OUT OF SCOPE
    # ─────────────────────────────────────────────────────────────────────────
    if _is_out_of_scope(q):
        return _add_confidence({"intent": "OUT_OF_SCOPE"}, 0.99)

    # ─────────────────────────────────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────────────────────────────────
    if _has_any_keyword(q, SUMMARY_KEYWORDS):
        return _add_confidence({"intent": "SUMMARY"}, 0.95)

    # ─────────────────────────────────────────────────────────────────────────
    # RECOMMENDATION
    # ─────────────────────────────────────────────────────────────────────────
    if _has_any_keyword(q, RECOMMENDATION_KEYWORDS):
        return _add_confidence({"intent": "RECOMMENDATION"}, 0.90)

    # ─────────────────────────────────────────────────────────────────────────
    # GENERAL CONCEPTUAL QUESTIONS
    # e.g. "difference between technical and hr round"
    # ─────────────────────────────────────────────────────────────────────────
    if _has_any_keyword(q, CONCEPTUAL_KEYWORDS):
        return _add_confidence({"intent": "GENERAL"}, 0.90)

    # ─────────────────────────────────────────────────────────────────────────
    # SINGLE_METRIC (e.g., "technical score of John" or "hr evaluation of Alice")
    # ─────────────────────────────────────────────────────────────────────────
    for metric_key in COLUMN_MAP.keys():
        if metric_key in q:
            pattern = rf'{re.escape(metric_key)}\s+(?:of|for|about)\s+(.+)'
            match = re.search(pattern, q)
            if match:
                name_val = match.group(1).strip()
                return _add_confidence({
                    "intent": "SINGLE_METRIC",
                    "metric": metric_key,
                    "name": name_val
                }, 0.92)

    # ─────────────────────────────────────────────────────────────────────────
    # BEST_WORST_ROUND (high priority)
    # Examples: "which round did X score worst", "scored the most in which round"
    # Only triggers if "round" or "which" keywords are present
    # ─────────────────────────────────────────────────────────────────────────
    if _has_any_keyword(q, BEST_WORST_KEYWORDS) and ("round" in q or "which" in q):
        # Try regex pattern first for "round|for|about|of Name"
        name_match = REGEX_NAME_EXTRACTION.search(q)
        extracted_name = name_match.group(1) if name_match else None

        # If not found, clean query and extract remaining words
        if not extracted_name:
            clean_query = re.sub(
                r'\b(out|of|4|rounds|in|which|round|scored|the|less|least|most|best|worst|minimal|maximal|highest|lowest|maximum|minimum)\b',
                '',
                q
            ).strip()
            if clean_query:
                extracted_name = clean_query

        # Even without explicit name, if "which round" or "in which round" is present, it's BEST_WORST_ROUND
        if extracted_name or ("which round" in q or "in which round" in q):
            if not extracted_name:
                extracted_name = "candidate"  # Generic name for "which round" queries
            direction = _get_direction(q)
            return _add_confidence({
                "intent": "BEST_WORST_ROUND",
                "name": extracted_name,
                "direction": direction
            }, 0.88)

    # ─────────────────────────────────────────────────────────────────────────
    # COMPARE and COMPARE_TOP (check before ROLE) - NOT if it's a BETWEEN or MULTI_FILTER pattern
    # Examples: "compare top 5 ML engineers", "John vs Alice", "compare top performers"
    # ─────────────────────────────────────────────────────────────────────────
    # Check if this is a MULTI_FILTER or BETWEEN pattern first
    is_multi_filter = bool(REGEX_MULTI_FILTER.search(q))
    is_between = bool(REGEX_BETWEEN.search(q))
    
    # Try COMPARE_TOP first (prioritize comparison patterns)
    if (("compare" in q or "comparison" in q or "versus" in q or "vs" in q) and "top" in q) or \
       ("which" in q and "top" in q and "best" in q):
        # Extract limit (default to 5)
        num_match = REGEX_NUMBER.search(q)
        limit = int(num_match.group(1)) if num_match else 5
        
        # Check if it mentions "performers", "candidates", or "best"
        if "performer" in q or "candidate" in q or ("best" in q and "which" in q):
            return _add_confidence({
                "intent": "COMPARE_TOP",
                "role": None,  # Generic, not role-specific
                "limit": limit
            }, 0.85)
        
        # Extract role
        potential_roles = _extract_potential_roles(q)
        if potential_roles:
            role_norm, _, _ = get_closest_role(potential_roles[0])
            if role_norm:
                return _add_confidence({
                    "intent": "COMPARE_TOP",
                    "role": role_norm,
                    "limit": limit
                }, 0.87)
    
    # Also handle "top N role comparison/vs" patterns even without "compare" keyword
    if "top" in q and ("comparison" in q or "versus" in q or "vs" in q):
        num_match = REGEX_NUMBER.search(q)
        limit = int(num_match.group(1)) if num_match else 5
        
        # Check for performers/candidates first
        if "performer" in q or "candidate" in q:
            return _add_confidence({
                "intent": "COMPARE_TOP",
                "role": None,
                "limit": limit
            }, 0.85)
        
        # Extract role
        potential_roles = _extract_potential_roles(q)
        if potential_roles:
            role_norm, _, _ = get_closest_role(potential_roles[0])
            if role_norm:
                return _add_confidence({
                    "intent": "COMPARE_TOP",
                    "role": role_norm,
                    "limit": limit
                }, 0.87)
    
    if (("compare" in q or " vs " in q or " versus " in q or " and " in q or " or " in q or " & " in q) and 
        not is_multi_filter and not is_between):
        # Try two-candidate comparison patterns
        name_part = q.replace("compare", "").strip()
        names = []
        
        if " and " in name_part:
            # Filter out role names from the and split
            parts = [n.strip() for n in name_part.split(" and ")]
            # Only treat as comparison if they look like names (not just keywords)
            if len(parts) == 2 and not any(keyword in p for p in parts for keyword in ["role", "engineer", "manager", "analyst", "developer"]):
                names = parts
        elif " & " in name_part or "&" in name_part:
            parts = [n.strip() for n in re.split(r'\s*&\s*', name_part) if n.strip()]
            if len(parts) == 2 and not any(keyword in p for p in parts for keyword in ["role", "engineer", "manager", "analyst", "developer"]):
                names = parts
        elif " or " in name_part:
            # Handle "or" as well
            parts = [n.strip() for n in name_part.split(" or ")]
            if len(parts) == 2 and not any(keyword in p for p in parts for keyword in ["role", "engineer", "manager", "analyst", "developer"]):
                names = parts
        elif " vs " in name_part:
            names = [n.strip() for n in name_part.split(" vs ")]
        elif " versus " in name_part:
            names = [n.strip() for n in name_part.split(" versus ")]

        if len(names) >= 2:
            return _add_confidence({
                "intent": "COMPARE",
                "names": names[:2]
            }, 0.85)

    # ─────────────────────────────────────────────────────────────────────────
    # TOP_METRIC (before comparing to avoid confusion with "who scored")
    # Handles: "highest technical score", "who scored lowest hr", "most points in pm"
    # ─────────────────────────────────────────────────────────────────────────
    if _has_any_keyword(q, ["highest", "lowest", "best", "worst", "maximum", "minimum", "most", "least"]):
        metric_keys = list(COLUMN_MAP.keys())
        for metric_key in sorted(metric_keys, key=len, reverse=True):
            if metric_key in q and "round" not in q:  # Don't confuse with BEST_WORST_ROUND
                direction = _get_direction(q)
                return _add_confidence({
                    "intent": "TOP_METRIC",
                    "metric": metric_key,
                    "direction": direction
                }, 0.83)
        
        # Also check for short metric names (technical, hr, pm, written)
        for col_abbrev in ["technical", "hr", "pm", "written"]:
            if col_abbrev in q and "round" not in q:
                direction = _get_direction(q)
                return _add_confidence({
                    "intent": "TOP_METRIC",
                    "metric": col_abbrev,
                    "direction": direction
                }, 0.83)

    # ─────────────────────────────────────────────────────────────────────────
    # MULTI_FILTER (e.g., "technical >20 and hr >20") - CHECK BEFORE COMPARE
    # ─────────────────────────────────────────────────────────────────────────
    multi_match = REGEX_MULTI_FILTER.search(q)
    if multi_match:
        return _add_confidence({
            "intent": "MULTI_FILTER",
            "filters": [
                {"metric": multi_match.group(1), "op": multi_match.group(2), "value": int(multi_match.group(3))},
                {"metric": multi_match.group(4), "op": multi_match.group(5), "value": int(multi_match.group(6))}
            ]
        }, 0.86)

    # ─────────────────────────────────────────────────────────────────────────
    # ANALYTICS / ROLE_ANALYTICS (e.g., "distribution by role")
    # ─────────────────────────────────────────────────────────────────────────
    if _has_any_keyword(q, ANALYTICS_KEYWORDS):
        if "role" in q:
            return _add_confidence({"intent": "ROLE_ANALYTICS"}, 0.82)
        else:
            return _add_confidence({"intent": "ANALYTICS"}, 0.80)

    # ─────────────────────────────────────────────────────────────────────────
    # ROUND_FILTER (metric-based filtering on rounds)
    # ─────────────────────────────────────────────────────────────────────────
    for metric_key, col in COLUMN_MAP.items():
        if metric_key in q:
            if _has_any_keyword(q, ["high", "low", "above", "below", "greater", "less", ">", "<", "scored", "score", "has", "got", "with"]):
                op = ">"
                val = 25 if _has_any_keyword(q, ["high", "above", "greater", ">"]) else 15
                
                num_match = REGEX_NUMBER.search(q)
                if num_match:
                    val = int(num_match.group(1))
                elif _has_any_keyword(q, ["low", "below", "less", "<"]):
                    op = "<"
                    val = 25

                # Override op based on keywords
                if _has_any_keyword(q, ["low", "below", "less", "<"]):
                    op = "<"
                if _has_any_keyword(q, ["scored", "has", "got", "with", "score"]) and \
                   not _has_any_keyword(q, ["above", "below", "greater", "less", ">", "<"]):
                    op = "="

                is_count = _is_count_query(q)
                return _add_confidence({
                    "intent": "ROUND_FILTER",
                    "metric": metric_key,
                    "column": col,
                    "op": op,
                    "value": val,
                    "is_count": is_count
                }, 0.79)

    # ─────────────────────────────────────────────────────────────────────────
    # COUNT (e.g., "how many candidates passed", "number of ML engineers")
    # ─────────────────────────────────────────────────────────────────────────
    if _is_count_query(q) and "scored" not in q:  # Don't treat "how many scored 20" as COUNT
        status = None
        role = None

        # Detect status
        for status_key, status_val in STATUS_KEYWORDS.items():
            if status_key in q:
                status = status_val
                break

        # Detect role
        potential_roles = _extract_potential_roles(q)
        if potential_roles:
            role, _, _ = get_closest_role(potential_roles[0])

        return _add_confidence({
            "intent": "COUNT",
            "status": status,
            "role": role
        }, 0.81)

    # ─────────────────────────────────────────────────────────────────────────
    # ROLE (e.g., "ML engineers", "top 5 backend developers")
    # ─────────────────────────────────────────────────────────────────────────
    potential_roles = _extract_potential_roles(q)
    if potential_roles:
        role_key = potential_roles[0]
        role_norm, is_exact, _ = get_closest_role(role_key)
        if role_norm:
            limit = _extract_limit(q)
            return _add_confidence({
                "intent": "ROLE",
                "role": role_norm,
                "limit": limit,
                "is_exact": is_exact,
                "original_role": role_key
            }, 0.85 if is_exact else 0.78)

    # ─────────────────────────────────────────────────────────────────────────
    # NAME / CANDIDATE SEARCH (e.g., "tell me about John", "show me Alice")
    # ─────────────────────────────────────────────────────────────────────────
    for trigger in sorted(NAME_TRIGGERS, key=len, reverse=True):
        if trigger in q:
            if re.search(rf'\b{re.escape(trigger)}\b', q):
                name_str = _extract_name_from_query(q, trigger)

                if not name_str:
                    continue

                # Check if it's actually a role
                role_norm, is_exact, _ = get_closest_role(name_str)
                if role_norm and is_exact:
                    return _add_confidence({
                        "intent": "ROLE",
                        "role": role_norm,
                        "limit": 5,
                        "is_exact": True
                    }, 0.89)

                return _add_confidence({
                    "intent": "NAME",
                    "name": name_str
                }, 0.79)

    # ─────────────────────────────────────────────────────────────────────────
    # PERFORMANCE (e.g., "top performers", "best scorers", "top 10 candidates")
    # ─────────────────────────────────────────────────────────────────────────
    if any(phrase in q for phrase in ["top performer", "top scorers", "best scorer", "top candidate"]) or \
       (q in ["top performers", "best scorers"] or "top" in q):
        limit = _extract_limit(q)
        return _add_confidence({
            "intent": "PERFORMANCE",
            "limit": limit
        }, 0.77)

    # ─────────────────────────────────────────────────────────────────────────
    # FILTER (e.g., "score > 20", "score between 10 and 20")
    # ─────────────────────────────────────────────────────────────────────────
    # Check for "between" pattern first
    between_match = REGEX_BETWEEN.search(q)
    if between_match:
        return _add_confidence({
            "intent": "FILTER",
            "score_min": int(between_match.group(1)),
            "score_max": int(between_match.group(2)),
            "op": "between",
            "is_count": _is_count_query(q)
        }, 0.76)

    # Check for other comparison operators
    if _has_any_keyword(q, ["below", "under", "less than", "above", "over", "greater than", "<", ">", ">=", "<=", "scored", "score", "has", "got", "with"]):
        score_val = _extract_first_number(q)
        if score_val:
            op = ">"
            if _has_any_keyword(q, ["below", "under", "less than", "<", "<="]):
                op = "<"
            elif _has_any_keyword(q, ["above", "over", "greater than", ">", ">="]):
                op = ">="
            elif _has_any_keyword(q, ["scored", "score", "has", "got", "with"]) and \
                 not _has_any_keyword(q, ["above", "below", "greater", "less", ">", "<", ">=", "<="]):
                op = "="

            return _add_confidence({
                "intent": "FILTER",
                "score": score_val,
                "op": op,
                "is_count": _is_count_query(q)
            }, 0.75)

    # ─────────────────────────────────────────────────────────────────────────
    # STATUS (e.g., "pass", "fail", "pending")
    # ─────────────────────────────────────────────────────────────────────────
    for status_key, status_val in STATUS_KEYWORDS.items():
        if status_key in q:
            return _add_confidence({
                "intent": "STATUS",
                "status": status_val
            }, 0.74)

    # ─────────────────────────────────────────────────────────────────────────
    # DEFAULT FALLBACKS
    # ─────────────────────────────────────────────────────────────────────────
    if _has_any_keyword(q, HR_KEYWORDS):
        return _add_confidence({
            "intent": "PERFORMANCE",
            "limit": 5
        }, 0.70)

    if len(q.split()) <= 3 and not _has_any_keyword(q, ["the", "is", "for"]):
        return _add_confidence({
            "intent": "NAME",
            "name": q
        }, 0.68)

    # ─────────────────────────────────────────────────────────────────────────
    # FINAL FALLBACK
    # ─────────────────────────────────────────────────────────────────────────
    return _add_confidence({
        "intent": "OUT_OF_SCOPE"
    }, 0.50)
