from fastapi import FastAPI
import sys

app = FastAPI()

@app.get("/health")
async def health():
    return {
        "status": "minimal_operational",
        "python_version": sys.version,
        "sys_path": sys.path
    }
