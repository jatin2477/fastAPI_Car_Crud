from fastapi import FastAPI
from routes.car_route import car

app = FastAPI()

app.include_router(car, tags=["Car"], prefix="/cars")

