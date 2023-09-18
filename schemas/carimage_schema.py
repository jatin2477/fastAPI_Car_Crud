from pydantic import BaseModel

class CarImageBase(BaseModel):
    image: str

class CarImageCreate(CarImageBase):
    pass 

class CarImageResponse(BaseModel):
    id: int
    car_id: int
    