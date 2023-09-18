from pydantic import BaseModel, Field

class CarBase(BaseModel):
    name: str = Field(title="Car Name", description="This is car name")
    color: str = Field(title="Car Color", description="This is car color", default="white")
    price: int = Field(gt=0, title="Car Price", description="This is car price")
    # car_company: str = Field(title="Car Company", description="This is car company name")

class CarCreate(CarBase):
    pass 

class CarResponse(CarBase):
    id: int
    