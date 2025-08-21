# app.py
import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os

# --- Configuration ---
# IMPORTANT: Replace with the actual Run ID of your BEST model from MLflow UI!
# Example: MLFLOW_RUN_ID = "a1b2c3d4e5f67890abcd1234"
#MLFLOW_RUN_ID = "YOUR_BEST_MODEL_RUN_ID_HERE" # <--- REPLACE THIS LINE!
MLFLOW_RUN_ID = "e29e2b05b8e341d7809c89725c6797e9" # <--- REPLACE THIS LINE!


# Path to the model artifact within the run
MODEL_ARTIFACT_PATH = "model"

##Also test it with empty "" value
#MODEL_ARTIFACT_PATH = "final_model_pipeline"

# Construct the MLflow model URI
# If using a remote MLflow Tracking Server, update the tracking URI
# mlflow.set_tracking_uri("http://your_mlflow_server_ip:5000")
MODEL_URI = f"runs:/{MLFLOW_RUN_ID}/{MODEL_ARTIFACT_PATH}"

# Initialize FastAPI app
app = FastAPI(
    title="Titanic Survival Prediction API",
    description="API for predicting survival on the Titanic using an MLflow-logged model.",
    version="1.0.0"
)

# Global variable to hold the loaded model pipeline
model_pipeline = None

@app.on_event("startup")
async def load_model():
    """
    Load the MLflow model pipeline when the FastAPI application starts up.
    This ensures the model is loaded only once and is available for all requests.
    """
    global model_pipeline
    try:
        print(f"Loading model from MLflow URI: {MODEL_URI}")
        # Note: We use mlflow.sklearn.load_model because we logged it with mlflow.sklearn
        model_pipeline = mlflow.sklearn.load_model(MODEL_URI)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        # This will prevent the FastAPI app from starting if the model can't be loaded
        raise HTTPException(status_code=500, detail=f"Model failed to load: {e}. Check MLFLOW_RUN_ID and ensure MLflow UI is running correctly for local runs.")

# Define the input data schema using Pydantic
class TitanicPassenger(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str

    class Config:
        schema_extra = {
            "example": {
                "Pclass": 3,
                "Sex": "male",
                "Age": 28.0,
                "SibSp": 0,
                "Parch": 0,
                "Fare": 10.0,
                "Embarked": "S"
            }
        }

# Define the prediction endpoint
@app.post("/predict")
async def predict_survival(passenger: TitanicPassenger):
    """
    Predicts survival for a single Titanic passenger.
    """
    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet.")

    # Convert input Pydantic model to Pandas DataFrame
    # Ensure column names match those expected by your preprocessor (from training data)
    input_df = pd.DataFrame([passenger.model_dump()]) # For Pydantic v2 use .model_dump()

    try:
        prediction = model_pipeline.predict(input_df)[0]
        survival_status = "Survived" if prediction == 1 else "Not Survived"
        return {"prediction": int(prediction), "survival_status": survival_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

# Root endpoint for health check
@app.get("/")
async def read_root():
    return {"message": "Titanic Survival Prediction API is running."}
