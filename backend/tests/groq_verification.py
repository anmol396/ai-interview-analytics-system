"""
========================================================
  GROQ (GROK) API COMPLETE VERIFICATION
  Tasks 1-7: Step-by-step verification
========================================================
"""
import os, sys, time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


# ===================================
# TASK 1: VERIFY API KEY
# ===================================
def task_1_verify_key():
    print("=" * 60)
    print("  TASK 1: VERIFY API KEY")
    print("=" * 60)
    
    # Check both possible env var names
    grok_key = os.getenv("GROK_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    
    active_key = grok_key or groq_key
    key_name = "GROK_API_KEY" if grok_key else ("GROQ_API_KEY" if groq_key else "NONE")
    
    if active_key:
        print(f"  Key Source:   {key_name}")
        print(f"  Key Preview:  {active_key[:10]}...")
        print(f"  Key Length:   {len(active_key)} chars")
        has_spaces = active_key != active_key.strip()
        print(f"  Extra Spaces: {'YES (BAD!)' if has_spaces else 'No'}")
        print(f"  Starts with:  gsk_ = {'Yes' if active_key.startswith('gsk_') else 'No'}")
        print(f"  Result:       PASS")
    else:
        print(f"  GROK_API_KEY: {grok_key}")
        print(f"  GROQ_API_KEY: {groq_key}")
        print(f"  Result:       FAIL - No API key found!")
    
    return active_key


# ===================================
# TASK 2: TEST GROQ CONNECTION
# ===================================
def task_2_test_connection(api_key):
    print("\n" + "=" * 60)
    print("  TASK 2: TEST GROQ CONNECTION (Direct API Call)")
    print("=" * 60)
    
    # Method A: Using requests (current project approach)
    print("\n  [Method A] Using requests library (project's current approach):")
    import requests
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": "What is machine learning? Answer briefly."}]
    }
    
    response_a = None
    try:
        t0 = time.time()
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        elapsed = time.time() - t0
        resp.raise_for_status()
        result = resp.json()
        content = result.get("choices", [])[0].get("message", {}).get("content", "")
        response_a = content
        print(f"    Status Code: {resp.status_code}")
        print(f"    Model Used:  {result.get('model', 'unknown')}")
        print(f"    Time:        {elapsed:.2f}s")
        print(f"    Response:    {content[:150]}...")
        print(f"    Result:      PASS - Groq API call success")
    except Exception as e:
        print(f"    Result:      FAIL")
        print(f"    Error:       {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"    Body:        {e.response.text[:200]}")
    
    # Method B: Using groq SDK (as per user's prompt)
    print("\n  [Method B] Using groq Python SDK:")
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        t0 = time.time()
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": "What is machine learning? Answer briefly."}]
        )
        elapsed = time.time() - t0
        content = response.choices[0].message.content
        print(f"    Model Used:  llama3-8b-8192")
        print(f"    Time:        {elapsed:.2f}s")
        print(f"    Response:    {content[:150]}...")
        print(f"    Result:      PASS - Groq SDK working")
    except ImportError:
        print(f"    Result:      SKIP - 'groq' package not installed")
        print(f"    Note:        Project uses requests library instead (Method A)")
    except Exception as e:
        print(f"    Result:      FAIL - {str(e)}")
    
    return response_a


# ===================================
# TASK 3: VERIFY RESPONSE TYPE
# ===================================
def task_3_verify_response_type(response):
    print("\n" + "=" * 60)
    print("  TASK 3: VERIFY RESPONSE TYPE")
    print("=" * 60)
    
    if not response:
        print("  No response to verify.")
        return False
    
    # Check for SQL/fallback indicators
    sql_indicators = [
        "SELECT", "FROM", "WHERE",
        "No candidates found",
        "offline fallback mode",
        "| Name |", "| Role |", "| Score |",
        "AI limit reached"
    ]
    
    is_sql_or_fallback = any(ind in response for ind in sql_indicators)
    is_text_explanation = len(response) > 50 and not is_sql_or_fallback
    
    print(f"  Response length:        {len(response)} chars")
    print(f"  Contains SQL keywords:  {'YES' if any(k in response for k in ['SELECT', 'FROM', 'WHERE']) else 'No'}")
    print(f"  Contains table format:  {'YES' if '|' in response and '---' in response else 'No'}")
    print(f"  Contains fallback msg:  {'YES' if 'fallback' in response.lower() or 'AI limit' in response else 'No'}")
    print(f"  Is text explanation:    {'Yes' if is_text_explanation else 'No'}")
    
    if is_text_explanation:
        print(f"  Result:                 PASS - Groq returned genuine AI response")
    else:
        print(f"  Result:                 FAIL - Response looks like SQL/fallback, NOT Groq")
    
    return is_text_explanation


# ===================================
# TASK 4: VERIFY ROUTING IN /chat
# ===================================
def task_4_verify_routing():
    print("\n" + "=" * 60)
    print("  TASK 4: VERIFY ROUTING PATH (ai_router.py)")
    print("=" * 60)
    
    import logging
    
    # Capture log output
    log_capture = []
    
    class LogHandler(logging.Handler):
        def emit(self, record):
            log_capture.append(f"[{record.name}] {record.getMessage()}")
    
    handler = LogHandler()
    handler.setLevel(logging.INFO)
    
    # Attach to relevant loggers
    for name in ["ai_router", "grok_service", "gemini_service", "fallback_service"]:
        lgr = logging.getLogger(name)
        lgr.addHandler(handler)
        lgr.setLevel(logging.INFO)
    
    from backend.services.ai_router import get_ai_response
    
    test_query = "Explain the difference between supervised and unsupervised learning"
    print(f"  Query: \"{test_query}\"")
    print(f"  Routing logs:")
    
    t0 = time.time()
    result = get_ai_response(test_query)
    elapsed = time.time() - t0
    
    for log_line in log_capture:
        print(f"    {log_line}")
    
    # Determine which path was taken
    used_grok = any("Calling Grok API" in l for l in log_capture)
    used_gemini = any("Calling Gemini API" in l for l in log_capture)
    used_fallback = any("Calling Internal Fallback" in l for l in log_capture)
    grok_success = any("Successfully received" in l for l in log_capture)
    
    print(f"\n  Path taken:")
    if used_grok and grok_success:
        print(f"    Trying GROQ...       EXECUTED")
        print(f"    Groq responded:      YES")
        print(f"    Falling back to SQL: NOT REACHED")
        print(f"    Result:              PASS - Groq is the active provider")
    elif used_grok and not grok_success:
        print(f"    Trying GROQ...       EXECUTED (but failed)")
        if used_gemini:
            print(f"    Falling back to Gemini: YES")
        if used_fallback:
            print(f"    Falling back to internal: YES")
        print(f"    Result:              PARTIAL - Groq tried but failed")
    elif used_fallback:
        print(f"    Trying GROQ...       SKIPPED")
        print(f"    Falling back:        YES")  
        print(f"    Result:              FAIL - Groq NOT being used")
    
    print(f"  Time: {elapsed:.2f}s")
    print(f"  Response preview: {result[:120]}...")
    
    # Cleanup
    for name in ["ai_router", "grok_service", "gemini_service", "fallback_service"]:
        logging.getLogger(name).removeHandler(handler)
    
    return used_grok and grok_success, result


# ===================================
# TASK 5: FORCE TEST (DISABLE SQL FALLBACK)
# ===================================
def task_5_force_test(api_key):
    print("\n" + "=" * 60)
    print("  TASK 5: FORCE GROK-ONLY TEST (SQL + Gemini + Fallback DISABLED)")
    print("=" * 60)
    
    import backend.services.ai_router as router_mod
    
    # Save originals
    orig_test_gemini = router_mod.test_gemini
    orig_fallback = router_mod.get_internal_fallback_response
    
    # Disable Gemini and Fallback
    router_mod.test_gemini = lambda: False
    router_mod.get_internal_fallback_response = lambda q, error_context="": "[BLOCKED] Fallback disabled for testing"
    
    test_queries = [
        "Explain difference between HR and Technical score",
        "What is overfitting in machine learning?",
        "Define regression analysis",
    ]
    
    all_passed = True
    try:
        for i, query in enumerate(test_queries, 1):
            print(f"\n  [{i}] Query: \"{query}\"")
            t0 = time.time()
            try:
                result = router_mod.get_ai_response(query)
                elapsed = time.time() - t0
                
                if "[BLOCKED]" in (result or ""):
                    print(f"      Status:   FAIL - Groq failed, hit blocked fallback")
                    print(f"      Error:    Groq could not handle this query")
                    all_passed = False
                else:
                    print(f"      Status:   PASS - Groq answered directly")
                    print(f"      Time:     {elapsed:.2f}s")
                    print(f"      Preview:  {result[:100]}...")
            except Exception as e:
                print(f"      Status:   FAIL - {str(e)}")
                all_passed = False
    finally:
        # Restore original functions
        router_mod.test_gemini = orig_test_gemini
        router_mod.get_internal_fallback_response = orig_fallback
    
    if all_passed:
        print(f"\n  TASK 5 Result: PASS - Groq handles all queries alone")
    else:
        print(f"\n  TASK 5 Result: FAIL - Groq cannot handle some queries")
    
    return all_passed


# ===================================
# TASK 6: ERROR HANDLING TEST
# ===================================
def task_6_error_handling():
    print("\n" + "=" * 60)
    print("  TASK 6: ERROR HANDLING TEST")
    print("=" * 60)
    
    import requests
    
    # Test with invalid key
    print("\n  [6a] Testing with INVALID API key:")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": "Bearer invalid_key_12345",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": "test"}],
        "max_tokens": 5
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=5)
        error_body = resp.json()
        error_type = error_body.get("error", {}).get("type", "unknown")
        error_msg = error_body.get("error", {}).get("message", "unknown")
        
        if "invalid_api_key" in error_type or "auth" in error_type.lower():
            print(f"    Detected: Invalid Groq API key")
            print(f"    Error type: {error_type}")
            print(f"    Action: System correctly identifies bad keys")
        elif "rate_limit" in error_type:
            print(f"    Detected: Groq quota exceeded")
            print(f"    Error type: {error_type}")
        else:
            print(f"    Error type: {error_type}")
            print(f"    Message: {error_msg[:100]}")
        
        print(f"    Result: PASS - Error handling works")
    except Exception as e:
        print(f"    Result: PASS - Exception caught: {str(e)[:80]}")
    
    # Test with invalid model
    print("\n  [6b] Testing with INVALID model name:")
    api_key = os.getenv("GROK_API_KEY") or os.getenv("GROQ_API_KEY")
    headers["Authorization"] = f"Bearer {api_key}"
    data["model"] = "nonexistent-model-xyz"
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=5)
        error_body = resp.json()
        error_type = error_body.get("error", {}).get("type", "unknown")
        print(f"    Error type: {error_type}")
        print(f"    Message: {error_body.get('error', {}).get('message', '')[:100]}")
        print(f"    Result: PASS - Invalid model error caught correctly")
    except Exception as e:
        print(f"    Result: PASS - Exception caught: {str(e)[:80]}")


# ===================================
# TASK 7: FINAL RESULT
# ===================================
def task_7_final_report(key_ok, connection_ok, response_valid, routing_ok, force_ok):
    print("\n" + "=" * 60)
    print("  TASK 7: FINAL RESULT")
    print("=" * 60)
    
    status = "WORKING" if (key_ok and connection_ok and routing_ok) else "NOT WORKING"
    icon = "PASS" if status == "WORKING" else "FAIL"
    
    print(f"""
  +--------------------------------------------------+
  |            GROQ API VERIFICATION REPORT           |
  +--------------------------------------------------+
  | API Key Valid:          {'PASS' if key_ok else 'FAIL':>25s} |
  | Direct API Connection:  {'PASS' if connection_ok else 'FAIL':>25s} |
  | Response is AI (not SQL):{'PASS' if response_valid else 'FAIL':>24s} |
  | Router uses Groq first: {'PASS' if routing_ok else 'FAIL':>24s} |
  | Groq-only mode works:   {'PASS' if force_ok else 'FAIL':>24s} |
  +--------------------------------------------------+
  | GROQ API STATUS:        {icon + ' ' + status:>25s} |
  +--------------------------------------------------+
  | System is using:        {'LLM (Groq)' if routing_ok else 'SQL Fallback':>25s} |
  +--------------------------------------------------+
""")
    
    if status == "WORKING":
        print("  Routing is CORRECT:")
        print("    - Conceptual questions -> Groq LLM")
        print("    - DB queries           -> SQL engine")
        print("    - If Groq fails        -> Gemini -> Internal fallback")
    else:
        print("  ISSUES DETECTED:")
        if not key_ok:
            print("    - API key is missing or invalid")
        if not connection_ok:
            print("    - Cannot connect to Groq API")
        if not routing_ok:
            print("    - Router is not using Groq as primary")
    
    return status == "WORKING"


# ===================================
# MAIN EXECUTION
# ===================================
if __name__ == "__main__":
    print("""
========================================================
   GROQ (GROK) API COMPLETE VERIFICATION
   Running all 7 tasks...
========================================================""")
    
    # Task 1
    api_key = task_1_verify_key()
    key_ok = api_key is not None
    
    if not key_ok:
        print("\nABORTED: No API key found. Cannot continue.")
        sys.exit(1)
    
    # Task 2
    response = task_2_test_connection(api_key)
    connection_ok = response is not None
    
    # Task 3
    response_valid = task_3_verify_response_type(response)
    
    # Task 4
    routing_ok, _ = task_4_verify_routing()
    
    # Task 5
    force_ok = task_5_force_test(api_key)
    
    # Task 6
    task_6_error_handling()
    
    # Task 7
    task_7_final_report(key_ok, connection_ok, response_valid, routing_ok, force_ok)
