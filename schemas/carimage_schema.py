from pydantic import BaseModel, Field

class CarImageBase(BaseModel):
    image: str
    image_size: str = Field(default="medium")
class CarImageCreate(CarImageBase):
    pass 

class CarImageResponse(CarImageBase):
    id: int
    car_id: int
