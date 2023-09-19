from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from models.car_model import CarModel
from schemas.car_schema import CarCreate, CarResponse
from passlib.context import CryptContext

car = APIRouter()

# Create a CryptContext instance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@car.get('/')
async def get_car(db: Session =  Depends(get_db)):
    return db.query(CarModel).all()
    
@car.get('/{car_id}', response_model=CarResponse)
async def get_car(car_id: int, db: Session =  Depends(get_db)):
    get_car = db.query(CarModel).filter(CarModel.id == car_id).first()
    if not get_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return get_car


@car.post('/add/', response_model=CarResponse)
async def add_car(car: CarCreate,db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = pwd_context.hash(car.car_company)
    car = CarModel(
                name=car.name,
                color=car.color,
                price=car.price,
                car_company=hashed_password,
            )
    db.add(car)
    db.commit()
    db.refresh(car)
    return car

@car.put('/edit/{car_id}')
async def update_car(car_id: int, updated_car: CarCreate, db: Session = Depends(get_db)):
    get_car = db.query(CarModel).filter(CarModel.id == car_id).first()

    if not get_car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    for key, value in updated_car.model_dump().items():
        setattr(get_car, key, value)

    db.commit()
    db.refresh(get_car)
    return get_car

@car.delete('/delete/{car_id}')
async def delete_car(car_id: int, db: Session = Depends(get_db)):
    remove_car = db.query(CarModel).filter(CarModel.id == car_id).first()

    if not remove_car:
        raise HTTPException(status_code=404, detail="Car not found")
        
    db.delete(remove_car)
    db.commit()
    db.refresh(remove_car)
    return remove_car