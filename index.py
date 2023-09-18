from fastapi import FastAPI
from routes.car_route import car
from routes.carimage_route import carimage

app = FastAPI()

app.include_router(car, tags=["Car"], prefix="/cars")
app.include_router(carimage, tags=["Car Image"], prefix="/images")

