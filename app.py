from fastapi import FastAPI

app = FastAPI(title="MLOps Pipeline API")

@app.get("/")
def home():
    return {"message": "MLOps Project Scaffolding Ready!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}