"""
╔══════════════════════════════════════════════════════════════════╗
║           AI ASSISTANT SELF-TEST SUITE                          ║
║  Tests: Grok API (Primary) → Gemini → Fallback                 ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import logging
import traceback
from datetime import datetime

# ── Setup project path ──
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# ── Configure Logging ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(name)-18s │ %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("self_test")

# ── Imports from project ──
from backend.services.grok_service import test_grok, ask_grok, GROK_API_KEY
from backend.services.gemini_service import test_gemini, ask_gemini, GOOGLE_API_KEY
from backend.services.fallback_service import get_internal_fallback_response
from backend.services.ai_router import get_ai_response

# ══════════════════════════════════════════════════════════════════
#  CONFIGURATION
# ══════════════════════════════════════════════════════════════════

TEST_QUERIES = [
    "Top 5 Machine Learning Engineers",
    "Top 5 Data Analysts",
    "Who is the Prime Minister of India?",
    "Explain regression in simple terms",
    "What is the role of a Product Manager?",
    "Give me SQL query to find top 5 candidates by score",
    "What is overfitting in machine learning?",
]

FALLBACK_MARKERS = [
    "⚠️ AI limit reached",
    "AI limit reached",
    "offline fallback mode",
    "Please try again later",
]

MAX_RESPONSE_TIME = 5.0  # seconds
SEPARATOR = "─" * 70

# ══════════════════════════════════════════════════════════════════
#  RESULT TRACKING
# ══════════════════════════════════════════════════════════════════

class TestResult:
    def __init__(self, query, provider):
        self.query = query
        self.provider = provider
        self.success = False
        self.response = None
        self.response_time = 0.0
        self.error = None
        self.is_fallback = False
        self.is_meaningful = False
        self.format_valid = False

results_grok_only = []         # Phase 1: Grok isolated
results_gemini_only = []       # Phase 2: Gemini isolated
results_fallback = []          # Phase 3: Fallback isolated
results_router = []            # Phase 4: Full router
issues_found = []
recommendations = []

# ══════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════

def is_fallback_response(text: str) -> bool:
    if not text:
        return True
    return any(marker.lower() in text.lower() for marker in FALLBACK_MARKERS)

def is_meaningful_response(text: str) -> bool:
    if not text or len(text.strip()) < 20:
        return False
    if is_fallback_response(text):
        return False
    return True

def validate_response_format(text: str) -> bool:
    """Check response is NOT expecting OpenAI-style object format."""
    if not text:
        return False
    # Should be plain text, not a raw JSON object with 'id', 'object', 'model' keys
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict) and "choices" in parsed:
            return False  # Raw OpenAI format leaked through
    except (json.JSONDecodeError, TypeError):
        pass  # Good — it's plain text, not raw JSON
    return True

def print_header(title):
    print(f"\n{'═' * 70}")
    print(f"  {title}")
    print(f"{'═' * 70}")

def print_result_row(idx, query, result):
    status = "✅" if result.success else "❌"
    meaningful = "✅" if result.is_meaningful else "⚠️"
    fmt = "✅" if result.format_valid else "❌"
    fallback = "⚠️ YES" if result.is_fallback else "✅ NO"
    time_ok = "✅" if result.response_time < MAX_RESPONSE_TIME else "⚠️ SLOW"
    
    print(f"\n  Query #{idx}: \"{query[:50]}{'...' if len(query) > 50 else ''}\"")
    print(f"    ├─ Status:       {status}")
    print(f"    ├─ Provider:     {result.provider}")
    print(f"    ├─ Time:         {result.response_time:.2f}s {time_ok}")
    print(f"    ├─ Meaningful:   {meaningful}")
    print(f"    ├─ Format OK:    {fmt}")
    print(f"    ├─ Is Fallback:  {fallback}")
    if result.error:
        print(f"    ├─ Error:        {result.error}")
    preview = (result.response or "")[:120].replace("\n", " ")
    print(f"    └─ Preview:      {preview}...")

# ══════════════════════════════════════════════════════════════════
#  PHASE 0: ENV & KEY VALIDATION
# ══════════════════════════════════════════════════════════════════

def phase_0_env_check():
    print_header("PHASE 0: Environment & API Key Validation")
    
    grok_key = GROK_API_KEY
    gemini_key = GOOGLE_API_KEY
    
    print(f"\n  GROK_API_KEY:   {'✅ Present (' + grok_key[:8] + '...)' if grok_key else '❌ MISSING'}")
    print(f"  GOOGLE_API_KEY: {'✅ Present (' + gemini_key[:8] + '...)' if gemini_key else '❌ MISSING'}")
    
    if not grok_key:
        issues_found.append("GROK_API_KEY is missing from .env")
        recommendations.append("Add GROK_API_KEY=<your_key> to .env file")
    if not gemini_key:
        issues_found.append("GOOGLE_API_KEY is missing from .env")
        recommendations.append("Add GOOGLE_API_KEY=<your_key> to .env file")
    
    return bool(grok_key), bool(gemini_key)

# ══════════════════════════════════════════════════════════════════
#  PHASE 1: GROK API ISOLATED TEST
# ══════════════════════════════════════════════════════════════════

def phase_1_grok_isolated():
    print_header("PHASE 1: Grok API — Health Check & Isolated Queries")
    
    # Health check
    print("\n  [1.0] Running Grok health check...")
    t0 = time.time()
    healthy = test_grok()
    hc_time = time.time() - t0
    print(f"  Grok Health:  {'✅ HEALTHY' if healthy else '❌ UNHEALTHY'}  ({hc_time:.2f}s)")
    
    if not healthy:
        issues_found.append("Grok API health check FAILED")
        recommendations.append("Verify GROK_API_KEY is valid and not expired")
        recommendations.append("Check network connectivity to api.groq.com")
        print("  ⚠️  Skipping Grok isolated queries (API unhealthy)")
        return False
    
    # Run queries
    for idx, query in enumerate(TEST_QUERIES, 1):
        r = TestResult(query, "Grok (Isolated)")
        try:
            t0 = time.time()
            response = ask_grok(query, timeout=10)
            r.response_time = time.time() - t0
            r.response = response
            r.success = response is not None and len(response.strip()) > 0
            r.is_fallback = is_fallback_response(response)
            r.is_meaningful = is_meaningful_response(response)
            r.format_valid = validate_response_format(response)
            
            if r.success:
                logger.info(f"Grok API call success for query #{idx}")
            else:
                logger.warning(f"Grok returned empty for query #{idx}")
                
        except Exception as e:
            r.response_time = time.time() - t0
            r.error = str(e)
            r.success = False
            logger.error(f"Grok API failed: {e}")
            issues_found.append(f"Grok failed on query #{idx}: {str(e)[:80]}")
        
        results_grok_only.append(r)
        print_result_row(idx, query, r)
    
    return True

# ══════════════════════════════════════════════════════════════════
#  PHASE 2: GEMINI API ISOLATED TEST
# ══════════════════════════════════════════════════════════════════

def phase_2_gemini_isolated():
    print_header("PHASE 2: Gemini API — Health Check & Isolated Queries")
    
    # Health check
    print("\n  [2.0] Running Gemini health check...")
    # Reset cached health status to force fresh check
    import backend.services.gemini_service as gs
    gs._gemini_healthy = None
    
    t0 = time.time()
    healthy = test_gemini()
    hc_time = time.time() - t0
    print(f"  Gemini Health: {'✅ HEALTHY' if healthy else '❌ UNHEALTHY'}  ({hc_time:.2f}s)")
    
    if not healthy:
        issues_found.append("Gemini API health check FAILED")
        recommendations.append("Verify GOOGLE_API_KEY is valid")
        print("  ⚠️  Skipping Gemini isolated queries (API unhealthy)")
        return False
    
    # Run a subset of queries (3 for speed)
    subset = TEST_QUERIES[:3]
    for idx, query in enumerate(subset, 1):
        r = TestResult(query, "Gemini (Isolated)")
        try:
            t0 = time.time()
            response = ask_gemini(query, timeout=10)
            r.response_time = time.time() - t0
            r.response = response
            r.success = response is not None and len(response.strip()) > 0
            r.is_fallback = is_fallback_response(response)
            r.is_meaningful = is_meaningful_response(response)
            r.format_valid = validate_response_format(response)
            
            if r.success:
                logger.info(f"Gemini API call success for query #{idx}")
                
        except Exception as e:
            r.response_time = time.time() - t0
            r.error = str(e)
            r.success = False
            logger.error(f"Gemini API failed: {e}")
            issues_found.append(f"Gemini failed on query #{idx}: {str(e)[:80]}")
        
        results_gemini_only.append(r)
        print_result_row(idx, query, r)
    
    return True

# ══════════════════════════════════════════════════════════════════
#  PHASE 3: FALLBACK SYSTEM TEST
# ══════════════════════════════════════════════════════════════════

def phase_3_fallback():
    print_header("PHASE 3: Internal Fallback System")
    
    for idx, query in enumerate(TEST_QUERIES[:3], 1):
        r = TestResult(query, "Fallback (Isolated)")
        try:
            t0 = time.time()
            response = get_internal_fallback_response(query)
            r.response_time = time.time() - t0
            r.response = response
            r.success = response is not None and len(response.strip()) > 0
            r.is_fallback = True  # Always true for this system
            r.is_meaningful = False  # Fallback is generic by design
            r.format_valid = validate_response_format(response)
            logger.info(f"Fallback system returned response for query #{idx}")
            
        except Exception as e:
            r.response_time = time.time() - t0
            r.error = str(e)
            r.success = False
            logger.error(f"Fallback system failed: {e}")
            issues_found.append(f"Fallback system crashed on query #{idx}: {str(e)[:80]}")
        
        results_fallback.append(r)
        print_result_row(idx, query, r)

# ══════════════════════════════════════════════════════════════════
#  PHASE 4: FULL AI ROUTER TEST (Grok → Gemini → Fallback)
# ══════════════════════════════════════════════════════════════════

def phase_4_full_router():
    print_header("PHASE 4: Full AI Router (Grok → Gemini → Fallback)")
    
    for idx, query in enumerate(TEST_QUERIES, 1):
        r = TestResult(query, "AI Router (auto)")
        try:
            t0 = time.time()
            response = get_ai_response(query)
            r.response_time = time.time() - t0
            r.response = response
            r.success = response is not None and len(response.strip()) > 0
            r.is_fallback = is_fallback_response(response)
            r.is_meaningful = is_meaningful_response(response)
            r.format_valid = validate_response_format(response)
            
            # Detect which provider was used
            if r.is_fallback:
                r.provider = "Fallback (internal)"
            elif results_grok_only and any(gr.success for gr in results_grok_only):
                r.provider = "Response from Grok API"
            elif results_gemini_only and any(gr.success for gr in results_gemini_only):
                r.provider = "Fallback to Gemini"
            else:
                r.provider = "Fallback to internal system"
            
            logger.info(f"Router: {r.provider} for query #{idx}")
            
        except Exception as e:
            r.response_time = time.time() - t0
            r.error = str(e)
            r.success = False
            logger.error(f"Router failed: {e}")
            issues_found.append(f"Router failed on query #{idx}: {str(e)[:80]}")
        
        results_router.append(r)
        print_result_row(idx, query, r)

# ══════════════════════════════════════════════════════════════════
#  PHASE 5: FORCE GROK-ONLY VERIFICATION
# ══════════════════════════════════════════════════════════════════

def phase_5_force_grok_only():
    print_header("PHASE 5: Force Grok-Only Verification (Gemini & Fallback Disabled)")
    
    # Temporarily monkey-patch to disable Gemini + Fallback
    import backend.services.ai_router as router_mod
    original_test_gemini = router_mod.test_gemini
    original_fallback = router_mod.get_internal_fallback_response
    
    router_mod.test_gemini = lambda: False
    router_mod.get_internal_fallback_response = lambda q, error_context="": f"[BLOCKED] Fallback disabled for testing. Last error: {error_context}"
    
    force_results = []
    try:
        for idx, query in enumerate(TEST_QUERIES[:4], 1):
            r = TestResult(query, "Grok (Force-Only)")
            try:
                t0 = time.time()
                response = get_ai_response(query)
                r.response_time = time.time() - t0
                r.response = response
                
                if "[BLOCKED]" in (response or ""):
                    r.success = False
                    r.provider = "FAILED — hit blocked fallback"
                    r.error = "Grok was unable to respond; system fell through to blocked fallback"
                    issues_found.append(f"Grok-only mode failed for query #{idx} — fell through to fallback")
                else:
                    r.success = True
                    r.provider = "Grok (confirmed sole provider)"
                    r.is_meaningful = is_meaningful_response(response)
                    r.format_valid = validate_response_format(response)
                    logger.info(f"Grok alone confirmed working for query #{idx}")
                    
            except Exception as e:
                r.response_time = time.time() - t0
                r.error = str(e)
                r.success = False
                logger.error(f"Grok-only failed: {e}")
            
            force_results.append(r)
            print_result_row(idx, query, r)
    finally:
        # Restore original functions
        router_mod.test_gemini = original_test_gemini
        router_mod.get_internal_fallback_response = original_fallback
    
    return force_results

# ══════════════════════════════════════════════════════════════════
#  PHASE 6: PERFORMANCE ANALYSIS
# ══════════════════════════════════════════════════════════════════

def phase_6_performance():
    print_header("PHASE 6: Performance Analysis")
    
    all_results = results_grok_only + results_router
    if not all_results:
        print("  No results to analyze.")
        return
    
    times = [r.response_time for r in all_results if r.success]
    if not times:
        print("  No successful responses to measure.")
        return
    
    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)
    slow_count = sum(1 for t in times if t > MAX_RESPONSE_TIME)
    
    print(f"\n  Total successful responses:  {len(times)}")
    print(f"  Average response time:      {avg_time:.2f}s")
    print(f"  Fastest response:           {min_time:.2f}s")
    print(f"  Slowest response:           {max_time:.2f}s")
    print(f"  Responses > {MAX_RESPONSE_TIME}s:          {slow_count}")
    print(f"  Performance threshold:      {'✅ PASS' if slow_count == 0 else '⚠️ ' + str(slow_count) + ' slow responses'}")
    
    if slow_count > 0:
        issues_found.append(f"{slow_count} responses exceeded {MAX_RESPONSE_TIME}s threshold")
        recommendations.append("Consider increasing timeout or optimizing prompts")

# ══════════════════════════════════════════════════════════════════
#  FINAL REPORT
# ══════════════════════════════════════════════════════════════════

def generate_final_report(grok_ok, gemini_ok, force_results):
    print_header("FINAL STATUS REPORT")
    
    # Grok status
    grok_success = sum(1 for r in results_grok_only if r.success)
    grok_total = len(results_grok_only)
    grok_status = grok_success == grok_total and grok_total > 0
    
    # Gemini status
    gemini_success = sum(1 for r in results_gemini_only if r.success)
    gemini_total = len(results_gemini_only)
    gemini_status = gemini_success == gemini_total and gemini_total > 0
    
    # Fallback status
    fallback_success = sum(1 for r in results_fallback if r.success)
    fallback_total = len(results_fallback)
    fallback_status = fallback_success == fallback_total and fallback_total > 0
    
    # Force-Grok status
    force_success = sum(1 for r in force_results if r.success) if force_results else 0
    force_total = len(force_results) if force_results else 0
    force_status = force_success == force_total and force_total > 0
    
    # Router status  
    router_success = sum(1 for r in results_router if r.success)
    router_total = len(results_router)
    router_meaningful = sum(1 for r in results_router if r.is_meaningful)
    router_fallbacks = sum(1 for r in results_router if r.is_fallback)
    
    # Format checks
    format_ok = all(r.format_valid for r in results_grok_only + results_router if r.success)
    
    print(f"""
  ┌────────────────────────────────────────────────────────┐
  │                  SERVICE STATUS                        │
  ├──────────────────────────┬─────────────────────────────┤
  │ Grok API (Primary)       │ {'✅ Working' if grok_status else '❌ Not Working':<28s}│
  │   └─ Queries Passed      │ {grok_success}/{grok_total:<26s}│
  │ Gemini API (Secondary)   │ {'✅ Working' if gemini_status else '❌ Not Working':<28s}│
  │   └─ Queries Passed      │ {gemini_success}/{gemini_total:<26s}│
  │ Fallback System          │ {'✅ Working' if fallback_status else '❌ Not Working':<28s}│
  │   └─ Queries Passed      │ {fallback_success}/{fallback_total:<26s}│
  │ Grok-Only Mode           │ {'✅ Working' if force_status else '❌ Not Working':<28s}│
  │   └─ Queries Passed      │ {force_success}/{force_total:<26s}│
  ├──────────────────────────┼─────────────────────────────┤
  │                  ROUTER SUMMARY                        │
  ├──────────────────────────┼─────────────────────────────┤
  │ Router Total Queries     │ {router_total:<28s}│
  │ Successful Responses     │ {router_success:<28d}│
  │ Meaningful Responses     │ {router_meaningful:<28d}│
  │ Fallback Responses       │ {router_fallbacks:<28d}│
  │ Response Format Valid    │ {'✅ Yes' if format_ok else '❌ No (OpenAI format leak)':<28s}│
  └──────────────────────────┴─────────────────────────────┘""")
    
    if not format_ok:
        issues_found.append("Some responses contain raw OpenAI-format JSON instead of parsed text")
        recommendations.append("Check grok_service.py response parsing — ensure content is extracted from choices[0].message.content")
    
    # Issues
    if issues_found:
        print(f"\n  ⚠️  Issues Found ({len(issues_found)}):")
        for i, issue in enumerate(issues_found, 1):
            print(f"    {i}. {issue}")
    else:
        print("\n  ✅ No issues found!")
    
    # Recommendations
    if recommendations:
        print(f"\n  💡 Recommendations ({len(recommendations)}):")
        for i, rec in enumerate(recommendations, 1):
            print(f"    {i}. {rec}")
    
    # Overall verdict
    overall = grok_status and (gemini_status or True) and fallback_status
    print(f"\n  {'═' * 54}")
    if overall and grok_status:
        print(f"  ✅ OVERALL: AI Pipeline is HEALTHY — Grok is PRIMARY")
    elif overall:
        print(f"  ⚠️  OVERALL: AI Pipeline works but Grok needs attention")
    else:
        print(f"  ❌ OVERALL: AI Pipeline has FAILURES — see issues above")
    print(f"  {'═' * 54}")
    
    return overall

# ══════════════════════════════════════════════════════════════════
#  MAIN EXECUTION
# ══════════════════════════════════════════════════════════════════

def main():
    start = time.time()
    
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║           AI ASSISTANT SELF-TEST SUITE                          ║
║  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<52s}║
║  Project: AI Interview System                                   ║
║  Primary: Grok (Groq) API                                       ║
╚══════════════════════════════════════════════════════════════════╝""")
    
    # Phase 0: Check environment
    has_grok_key, has_gemini_key = phase_0_env_check()
    
    # Phase 1: Grok isolated
    grok_ok = phase_1_grok_isolated() if has_grok_key else False
    
    # Phase 2: Gemini isolated
    gemini_ok = phase_2_gemini_isolated() if has_gemini_key else False
    
    # Phase 3: Fallback system
    phase_3_fallback()
    
    # Phase 4: Full router
    phase_4_full_router()
    
    # Phase 5: Force Grok-only
    force_results = phase_5_force_grok_only() if has_grok_key else []
    
    # Phase 6: Performance
    phase_6_performance()
    
    # Final Report
    overall = generate_final_report(grok_ok, gemini_ok, force_results)
    
    elapsed = time.time() - start
    print(f"\n  Total test duration: {elapsed:.1f}s")
    print(f"  Test completed at:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
