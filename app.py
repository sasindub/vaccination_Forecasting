from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from model.predict_model import predict_demand
import pandas as pd
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Adding CORS middleware to allow requests from specific origins
origins = [
    "https://whfgrx3r-8000.asse.devtunnels.ms",  # Frontend origin 
    "http://localhost:8000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# Model for the request
class PredictionRequest(BaseModel):
    region: int
    month: int
    population: int
    prev_demand: int = None

# Model for the response
class DataPoint(BaseModel):
    label: str
    value: float

# Home route to render the HTML page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Prediction route 
@app.post("/predict")
async def predict(request: PredictionRequest):
    # Extract the data from the request model
    prediction = predict_demand(request.region, request.month, request.population, request.prev_demand)
    return {"predicted_demand": prediction}

# Chart page route
@app.get("/chart", response_class=HTMLResponse)
async def chart_page(request: Request):
    return templates.TemplateResponse("chart.html", {"request": request})


@app.get("/synthetic_vaccine_data", response_model=List[DataPoint])
async def get_synthetic_vaccine_data():
    # Read the CSV file
    df = pd.read_csv('synthetic_vaccine_data.csv')
    
  
    df_limited = df.head(50)
    print(f"Number of rows in the original dataset: {len(df_limited)}")

    data = [
        DataPoint(
            label=f"Month {int(row['month'])}, Region {int(row['region'])}",
            value=float(row['demand'])
        )
        for _, row in df_limited.iterrows()
    ]

    return data