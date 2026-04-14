"""
FastAPI web API — activate when deploying beyond localhost.
Uncomment fastapi/uvicorn in requirements.txt and run:
    uvicorn api.main:app --reload
"""
# from fastapi import FastAPI
# from prediction.predict import run_inference
# from gti.aggregator import compute_gti
#
# app = FastAPI(title="Geo-Market API")
#
# @app.get("/gti")
# def get_gti():
#     return compute_gti()
#
# @app.get("/predict")
# def get_prediction():
#     return run_inference()
