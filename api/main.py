"""
FastAPI web API — activate when deploying beyond localhost.
Uncomment fastapi/uvicorn in requirements.txt and run:
    uvicorn api.main:app --reload
"""
from fastapi import FastAPI
import requests
import os
from prediction.predict import run_inference
from gti.aggregator import compute_gti

app = FastAPI(title="Geo-Market API")

# MCP Stitch configuration
STITCH_URL = "https://stitch.googleapis.com/mcp"
STITCH_API_KEY = os.getenv("STITCH_API_KEY", "")

def get_ui_details(component: str):
    """Fetch UI details from Stitch MCP server."""
    url = f"{STITCH_URL}/ui/{component}"
    headers = {"X-Goog-Api-Key": STITCH_API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

@app.get("/gti")
def get_gti():
    return compute_gti()

@app.get("/predict")
def get_prediction():
    return run_inference()

@app.get("/ui/{component}")
def get_ui(component: str):
    """Get UI details for a component from Stitch MCP."""
    return get_ui_details(component)
