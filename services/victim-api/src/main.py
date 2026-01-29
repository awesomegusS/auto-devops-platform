from fastapi import FastAPI, HTTPException
import uvicorn
import os
import sys

app = FastAPI()

# Global variable to simulate a "healthy" state
is_healthy = True

@app.get("/")
def read_root():
    if not is_healthy:
        raise HTTPException(status_code=500, detail="Internal Server Error: Database Connection Failed")
    return {"status": "operational", "message": "System is running smoothly."}

@app.get("/chaos/crash")
def trigger_crash():
    """Simulates a critical failure (Process Exit)"""
    print("CRITICAL: Segment Fault detected. Shutting down...", file=sys.stderr)
    sys.exit(1)

@app.get("/chaos/disconnect")
def trigger_disconnect():
    """Simulates a logic error (500 Error loop)"""
    global is_healthy
    print("ERROR: Database connection timeout. Retrying...", file=sys.stderr)
    is_healthy = False
    return {"status": "system broken"}

@app.get("/health")
def health_check():
    if not is_healthy:
        raise HTTPException(status_code=503, detail="Unhealthy")
    return {"status": "ok"}

if __name__ == "__main__":
    # We bind to 0.0.0.0 so Docker can expose it
    uvicorn.run(app, host="0.0.0.0", port=8000)