import re
import difflib

# ─── HR CONFIGURATION ──────────────────────────────────────────────────────────
KNOWN_ROLES = ["ML Engineer", "Product Manager", "Data Analyst", "Backend Developer"]
ROLE_MAP = {
    "project manager": "product manager",
    "pm": "product manager",
    "backend dev": "backend developer",
    "ml": "ml engineer",
}

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

def get_closest_role(requested_role: str):
    """Returns (normalized_role, is_exact, suggested_role)"""
    requested_role = requested_role.lower().strip()
    
    # Check ROLE_MAP first
    if requested_role in ROLE_MAP:
        mapped = ROLE_MAP[requested_role]
        # Find original case
        for kr in KNOWN_ROLES:
            if kr.lower() == mapped.lower():
                return kr, False, kr
    
    # Check exact match in KNOWN_ROLES
    for kr in KNOWN_ROLES:
        if kr.lower() == requested_role:
            return kr, True, None
            
    # Fuzzy match
    matches = difflib.get_close_matches(requested_role, [r.lower() for r in KNOWN_ROLES], n=1, cutoff=0.5)
    if matches:
        for kr in KNOWN_ROLES:
            if kr.lower() == matches[0]:
                return kr, False, kr
                
    return None, False, None

def classify_query(query: str) -> dict:
    """Classify user query into exactly ONE intent type."""
    # Pre-clean the query
    q = query.lower().strip()
    q = re.sub(r'[?.,!;:]', ' ', q).strip()
    q = re.sub(r'\s+', ' ', q)

    # ── DEFENSIVE GUARD: OUT OF SCOPE ──
    OUT_OF_SCOPE_KEYWORDS = [
        "prime minister", "weather", "elon musk", "president", 
        "news", "stock price", "capital of", "politics", "india", 
        "price of", "crypto", "bitcoin", "football", "cricket"
    ]
    if any(re.search(rf'\b{re.escape(word)}\b', q) for word in OUT_OF_SCOPE_KEYWORDS):
        return {"intent": "OUT_OF_SCOPE"}

    # ── SUMMARY ──
    if any(w in q for w in ["summary", "overall performance", "stats", "statistics"]):
        return {"intent": "SUMMARY"}

    # ── RECOMMENDATION ──
    if any(w in q for w in ["recommend", "best candidate", "hire", "should we hire", "suggest", "best fit"]):
        return {"intent": "RECOMMENDATION"}

    # ── SINGLE METRIC SEARCH (Score of Name) ──
    for metric_key in COLUMN_MAP.keys():
        if metric_key in q:
            matches = re.search(rf'{re.escape(metric_key)}\s+(?:of|for|about)\s+(.+)', q)
            if matches:
                name_val = matches.group(1).strip()
                return {"intent": "SINGLE_METRIC", "metric": metric_key, "name": name_val}

    # ── ROUND FILTER ──
    for metric_key, col in COLUMN_MAP.items():
        if metric_key in q:
            if any(w in q for w in ["high", "low", "above", "below", "greater", "less", ">", "<", "scored", "score", "has", "got", "with"]):
                op = ">"
                val = 25 if "high" in q or "above" in q or "greater" in q or ">" in q else 15
                num_match = re.search(r'(\d+)', q)
                if num_match: 
                    val = int(num_match.group(1))
                elif "low" in q or "below" in q or "less" in q or "<" in q:
                    op = "<"
                    val = 25
                
                if any(w in q for w in ["low", "below", "less", "<"]): op = "<"
                if any(w in q for w in ["scored", "has", "got", "with", "score"]) and not any(w in q for w in ["above", "below", "greater", "less", ">", "<"]): op = "="
                
                is_count = any(w in q for w in ["how many", "count", "number of"])
                return {"intent": "ROUND_FILTER", "metric": metric_key, "column": col, "op": op, "value": val, "is_count": is_count}

    # ── BEST/WORST ROUND ──
    if any(w in q for w in ["best round", "worst round", "lowest score", "highest score", "scored the less", "scored the most", "scored the least", "which round"]):
        name_match = re.search(r'(?:round|for|about|of)\s+([a-z]+\s+[a-z]+)', q)
        extracted_name = name_match.group(1) if name_match else None
        if not extracted_name:
            clean = re.sub(r'\b(out|of|4|rounds|in|which|round|scored|the|less|least|most|best|worst|minimal|maximal|highest|lowest)\b', '', q).strip()
            if clean: extracted_name = clean
            
        if extracted_name:
            direction = "worst" if any(w in q for w in ["less", "least", "worst", "lowest", "minimal", "min"]) else "best"
            if any(w in q for w in ["best", "most", "max", "highest"]) and any(w in q for w in ["worst", "less", "least", "low", "min"]):
                direction = "both"
            return {"intent": "BEST_WORST_ROUND", "name": extracted_name, "direction": direction}

    # ── COMPARE ──
    if "compare" in q:
        top_match = re.search(r'compare\s+top\s+(\d+)\s+(.+)', q)
        if top_match:
            limit = int(top_match.group(1))
            role_str = top_match.group(2).strip().replace("from that", "").replace("from them", "").strip()
            if role_str:
                role_norm, _, _ = get_closest_role(role_str)
                if role_norm:
                    return {"intent": "COMPARE_TOP", "role": role_norm, "limit": limit}

        names = []
        name_part = q.replace("compare", "").strip()
        if " and " in name_part:
            names = [n.strip() for n in name_part.split(" and ")]
        elif " vs " in name_part:
            names = [n.strip() for n in name_part.split(" vs ")]
        
        if len(names) >= 2:
            return {"intent": "COMPARE", "names": names[:2]}

    # ── ANALYTICS ──
    if any(w in q for w in ["distribution", "by role", "role count", "role wise", "each role", "role-wise"]):
        return {"intent": "ANALYTICS"}

    # ── COUNT ──
    if any(w in q for w in ["how many", "count", "number of"]) or ("total" in q and "score" not in q):
        status, role = None, None
        if "pass" in q: status = "passed"
        elif "fail" in q: status = "failed"
        elif "pending" in q: status = "pending"
        
        potential_roles = list(ROLE_MAP.keys()) + [r.lower() for r in KNOWN_ROLES]
        for r_key in sorted(potential_roles, key=len, reverse=True):
            if re.search(rf'\b{re.escape(r_key)}(?:s)?\b', q):
                role, _, _ = get_closest_role(r_key)
                break
        return {"intent": "COUNT", "status": status, "role": role}

    # ── NAME/ROLE SEARCH ──
    name_triggers = ["tell me about", "tell me", "role of", "details of", "who is", "about", "candidate", "identify", "role", "find", "profile of", "show me"]
    name_triggers.sort(key=len, reverse=True)
    for trigger in name_triggers:
        if trigger in q:
            if re.search(rf'\b{re.escape(trigger)}\b', q):
                name_str = q.replace(trigger, "").strip()
                if trigger in ["role", "details", "tell me", "profile"]:
                    name_str = re.sub(r'^(?:of|about)\s+', '', name_str).strip()
                if not name_str: continue
                role_norm, is_exact, suggestion = get_closest_role(name_str)
                if role_norm and is_exact:
                    return {"intent": "ROLE", "role": role_norm, "limit": 5, "is_exact": True}
                return {"intent": "NAME", "name": name_str}

    potential_roles = list(ROLE_MAP.keys()) + [r.lower() for r in KNOWN_ROLES]
    for r_key in sorted(potential_roles, key=len, reverse=True):
        if re.search(rf'\b{re.escape(r_key)}(?:s)?\b', q):
            role_norm, is_exact, suggestion = get_closest_role(r_key)
            if role_norm:
                limit_match = re.search(r'top\s+(\d+)', q)
                limit = int(limit_match.group(1)) if limit_match else 5
                return {"intent": "ROLE", "role": role_norm, "limit": limit, "is_exact": is_exact, "original_role": r_key}

    # ── TOP PERFORMERS ──
    if "top performer" in q or "top scorers" in q or q in ["top performers", "best scorers"] or "top" in q:
        limit_match = re.search(r'top\s+(\d+)', q)
        limit = int(limit_match.group(1)) if limit_match else 5
        return {"intent": "PERFORMANCE", "limit": limit}

    # ── FILTER ──
    if any(w in q for w in ["below", "under", "less than", "above", "over", "greater than", "<", ">", "scored", "score", "has", "got", "with"]):
        match = re.search(r'\d+', q)
        if match:
            op = ">"
            if any(w in q for w in ["below", "under", "less than", "<"]): op = "<"
            elif any(w in q for w in ["scored", "score", "has", "got", "with"]) and not any(w in q for w in ["above", "below", "greater", "less", ">", "<"]): op = "="
            return {"intent": "FILTER", "score": int(match.group()), "op": op, "is_count": any(w in q for w in ["how many", "count", "number of"])}

    # ── STATUS ──
    if "fail" in q: return {"intent": "STATUS", "status": "fail"}
    if "pending" in q: return {"intent": "STATUS", "status": "pending"}
    if "pass" in q: return {"intent": "STATUS", "status": "pass"}

    # ── GENERAL / CONCEPTUAL ──
    GENERAL_KEYWORDS = ["what", "who", "explain", "difference", "define", "why", "how", "tell me about"]
    # Only fallback to GENERAL if it doesn't contain data-rich keywords
    if (any(q.startswith(w) for w in GENERAL_KEYWORDS) or any(w in q for w in ["difference", "how to", "what is"])) and \
       not any(w in q for w in ["score", "many", "count", "candidate", "role", "performer", "best", "worst", "top", "list", "recommend", "hire"]):
        return {"intent": "GENERAL"}

    # Default fallback
    hr_words = ["candidate", "score", "interview", "hiring", "talent", "employee"]
    if any(w in q for w in hr_words): return {"intent": "PERFORMANCE"}
    if len(q.split()) <= 3 and not any(w in q for w in ["the", "is", "for"]): return {"intent": "NAME", "name": q}

    return {"intent": "OUT_OF_SCOPE"}
