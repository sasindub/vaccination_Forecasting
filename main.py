from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from model.predict_model import predict_demand  # Import prediction function
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Home
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def oredict(region: int, month: int, population: int, prev_demand: int):
    prediction = predict_demand(region, month, population, prev_demand)
    return {"predited_demand": prediction}
