import sys
import os

# Standard Python path fix for Vercel
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

try:
    from agents.api import app
except Exception as e:
    from fastapi import FastAPI
    app = FastAPI()
    @app.get("/")
    async def root():
        return {"status": "error", "msg": str(e)}
    @app.get("/health")
    async def health():
        return {"status": "error", "msg": str(e)}
