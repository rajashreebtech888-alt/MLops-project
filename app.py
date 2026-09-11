from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import pandas as pd
import io

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset

app = FastAPI()

@app.post("/analyze-visual/", response_class=HTMLResponse)
async def analyze_visual(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded dataset is empty.")

        # Generates quality and drift metrics against reference data
        report = Report(metrics=[DataQualityPreset(), DataDriftPreset()])
        report.run(reference_data=df, current_data=df)
        
        return HTMLResponse(content=report.get_html(), status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evidently AI Processing Error: {str(e)}")