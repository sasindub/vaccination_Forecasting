from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from model.predict_model import predict_demand
import pandas as pd
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# model for the request
class PredictionRequest(BaseModel):
    region: int
    month: int
    population: int
    prev_demand: int = None

# model for the response
class DataPoint(BaseModel):
    label: str
    value: float


# Home route to render the HTML page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Prediction route to accept JSON request body
@app.post("/predict")
async def predict(request: PredictionRequest):
    # Extract the data from the request model
    prediction = predict_demand(request.region, request.month, request.population, request.prev_demand)
    

    return {"predicted_demand": prediction}


@app.get("/chart", response_class=HTMLResponse)
async def chart_page(request: Request):
    return templates.TemplateResponse("chart.html", {"request": request})

@app.get("/synthetic_vaccine_data", response_model=List[DataPoint])
async def get_synthetic_vaccine_data():

    df = pd.read_csv('synthetic_vaccine_data.csv')

    
    data = []
    for _, row in df.iterrows():
        data.append(DataPoint(
            label=f"Month {int(row['month'])}, Region {int(row['region'])}",
            value=float(row['demand'])
        ))

    return data

