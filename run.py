import uvicorn
import os

if __name__ == "__main__":
    print("Starting AI HR Analytics Backend...")
    # This replaces the long command line string
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["backend"] # Only watch the backend folder
    )
