"""Quick verification: Gemini SDK migration from google-generativeai to google.genai"""
import sys, os, time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

print("=== Gemini SDK Migration Verification ===\n")

# 1. Check import
try:
    from google import genai
    print("[1] Import google.genai: PASS")
except Exception as e:
    print(f"[1] Import google.genai: FAIL - {e}")
    sys.exit(1)

# 2. Check service loads
try:
    from backend.services.gemini_service import test_gemini, ask_gemini, DEFAULT_GEMINI_MODEL
    print(f"[2] Service loaded: PASS (model={DEFAULT_GEMINI_MODEL})")
except Exception as e:
    print(f"[2] Service loaded: FAIL - {e}")
    sys.exit(1)

# 3. Health check
print("[3] Running health check...")
t0 = time.time()
healthy = test_gemini()
elapsed = time.time() - t0
status = "PASS" if healthy else "FAIL"
print(f"    Result: {status} ({elapsed:.2f}s)")

# 4. Generate content
if healthy:
    print('[4] Test query: "What is 2+2?"')
    t0 = time.time()
    try:
        resp = ask_gemini("What is 2+2? Answer in one word.", timeout=10)
        elapsed = time.time() - t0
        preview = resp.strip()[:100]
        print(f"    Response: {preview}")
        print(f"    Time: {elapsed:.2f}s")
        print("    Result: PASS")
    except Exception as e:
        print(f"    Result: FAIL - {e}")
else:
    print("[4] Skipped (health check failed)")

# 5. Full router test
print("[5] Testing full AI router...")
try:
    from backend.services.ai_router import get_ai_response
    t0 = time.time()
    resp = get_ai_response("Explain AI in one sentence")
    elapsed = time.time() - t0
    preview = resp.strip()[:100]
    print(f"    Response: {preview}")
    print(f"    Time: {elapsed:.2f}s")
    print("    Result: PASS")
except Exception as e:
    print(f"    Result: FAIL - {e}")

print("\n=== VERIFICATION COMPLETE ===")
