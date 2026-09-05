from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI(title="MLOps Pipeline API")

model = joblib.load("model.pkl")

@app.get("/")
def home():
    return {"message": "MLOps Model API is Live!"}

@app.post("/predict")
def predict(features: list[float]):
    data = np.array(features).reshape(1, -1)
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}
