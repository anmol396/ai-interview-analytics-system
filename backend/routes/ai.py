from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import re

from backend.database import get_db
from backend.services.auth import get_current_user
from backend.services.ai_router import ask_llm
from backend.services.ai_classifier import classify_query, KNOWN_ROLES, ROLE_MAP
from backend.services.ai_db_handler import handle_query_with_sql

router = APIRouter(prefix="/chat", tags=["ai_agent"])

class ChatRequest(BaseModel):
    query: str
    history: List[Dict[str, str]] = []
    provider: str = "auto"

@router.post("")
def chat_endpoint(
    req: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """
    Intelligent HR Analytics Assistant.
    Deterministic intent detection with LLM fallback.
    """
    # ── STEP 1: Compound Query Logic ──
    split_pattern = r'\s*(?:&|and then|then|\band\b(?=\s+(?:compare|show|tell|who|what|give|find|how|identify|recommend|summary|analytics|distribution|role|details|top|best|worst|count|describe|list)))\s*'
    query_parts = [p.strip() for p in re.split(split_pattern, req.query, flags=re.IGNORECASE) if p.strip()]
    
    final_data = None
    accumulated_responses = []
    last_context_role = None

    for i, q_part in enumerate(query_parts):
        processed_q = q_part
        if i > 0 and last_context_role:
            if any(w in processed_q.lower() for w in ["that", "those", "them", "result"]):
                processed_q = processed_q.replace("from that", last_context_role).replace("from them", last_context_role).replace("that", last_context_role)

        data = handle_query_with_sql(processed_q, db)
        
        if data.get("response") == "TRIGGER_LLM":
            try:
                llm_text = ask_llm(processed_q)
                accumulated_responses.append(llm_text)
                continue
            except Exception:
                accumulated_responses.append("Conceptual analysis currently unavailable.")
                continue

        if data.get("title") and "Top" in data["title"]:
            possible_role = data["title"].replace("Top", "").strip().rstrip("s")
            if possible_role: last_context_role = possible_role

        if data.get("response") and "process" not in data["response"].lower():
            accumulated_responses.append(data["response"])
            if not final_data: final_data = data

    if accumulated_responses:
        if not final_data: final_data = {"response": "", "title": "AI Response"}
        
        # Combine Markdown for legacy frontend compatibility
        combined_md = "\n\n".join(accumulated_responses)
        
        # Add AI Insight
        try:
            insight_prompt = f"Provide a single, short HR insight based on this data: {combined_md[:500]}"
            ai_insight = ask_llm(insight_prompt).replace("### Insight:", "").strip()
            combined_md += f"\n\n### AI Insight:\n\n{ai_insight}"
        except Exception: pass

        result = {
            "intent": "database" if final_data.get("data") else "llm",
            "response": combined_md,
            "title": final_data.get("title", "AI Assistant"),
            "structured_data": final_data.get("data", []), # New structured JSON format
            "metadata": {
                "total": final_data.get("total", 0),
                "has_more": final_data.get("has_more", False),
                "filter_key": final_data.get("filter_key")
            }
        }
        return result

    # ── STEP 2: Pure LLM Fallback ──
    try:
        llm_response = ask_llm(req.query)
        return {
            "response": llm_response,
            "intent": "llm",
            "title": "AI Assistant Response",
            "structured_data": []
        }
    except Exception:
        return {
            "response": "Service temporarily unavailable. Try asking about HR scores.",
            "intent": "error",
            "title": "System Busy"
        }

@router.get("/full-list")
def get_full_list(
    filter_key: str = Query(..., description="Filter key like 'score_<_50' or 'status_fail'"),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """Returns full candidate list for a given filter."""
    try:
        # Whitelist for safety
        allowed_cols = ["hr_evaluation", "technical_assessment", "written_test", "pm_assessment", "total_score"]
        
        if filter_key.startswith("score_"):
            parts = filter_key.split("_")
            
            # Format could be score_col_name_op_val (len >= 4) or score_op_val (len == 3)
            if len(parts) >= 4:
                val = int(parts[-1])
                op = parts[-2]
                col = "_".join(parts[1:-2])
            elif len(parts) == 3:
                val = int(parts[2])
                op = parts[1]
                col = "total_score"
            else:
                raise ValueError(f"Invalid score filter format: {filter_key}")
            
            if col not in allowed_cols: raise ValueError(f"Invalid column: {col}")
            sql = f"SELECT name, role, status, total_score FROM hr_candidates WHERE {col} {op} :v ORDER BY {col} DESC"
            rows = db.execute(text(sql), {"v": val}).fetchall()
            
        elif filter_key.startswith("status_"):
            status_val = filter_key.replace("status_", "")
            sql = "SELECT name, role, status, total_score FROM hr_candidates WHERE LOWER(status) LIKE :s ORDER BY total_score DESC"
            rows = db.execute(text(sql), {"s": f"%{status_val}%"}).fetchall()
            
        elif filter_key.startswith("role_"):
            role_val = filter_key.replace("role_", "")
            sql = "SELECT name, role, status, total_score FROM hr_candidates WHERE LOWER(role) LIKE :r"
            rows = db.execute(text(sql), {"r": f"%{role_val.lower()}%"}).fetchall()
            
        else: raise ValueError("Unknown filter_key")

        candidates = [{"name": r[0].replace("_", " "), "role": r[1], "status": r[2], "total_score": r[3]} for r in rows]
        return {"candidates": candidates, "total": len(candidates)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
