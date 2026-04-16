import sys
import os

# Add the current directory to sys.path so 'agents' can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agents.api import app
except Exception as e:
    from fastapi import FastAPI
    app = FastAPI()
    @app.get("/health")
    async def health():
        return {"status": "error", "message": str(e), "path": sys.path}
