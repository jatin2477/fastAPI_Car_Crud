from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from config.db import get_db
from models.carimage_model import CarImageModel
from schemas.carimage_schema import CarImageCreate, CarImageResponse
import os

carimage = APIRouter()

# Define the directory where you want to store the images
IMAGE_UPLOAD_DIR = "image_uploads"

# Ensure the directory exists
os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)
    
@carimage.get('/{car_id}', response_model=CarImageResponse)
async def get_car(car_id: int, db: Session =  Depends(get_db)):
    get_car = db.query(CarImageModel).filter(CarImageModel.id == car_id).first()
    if not get_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return get_car


@carimage.post('/add/{car_id}', response_model=CarImageResponse)
async def add_car(car_id: int,file: UploadFile,db: Session = Depends(get_db)):
    image_data = await file.read()
    #  # Generate a unique filename for the image
    # filename = file.filename
    # filepath = os.path.join(IMAGE_UPLOAD_DIR, filename)

    # # Save the image to the server
    # with open(filepath, "wb") as image_file:
    #     image_file.write(image_data)

    # Create a new ImageInfo instance with the filename and save it to the database
    car = CarImageModel(car_id=car_id, image=image_data)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car

#@carimage.put('/edit/{car_id}')
async def update_car(car_id: int, updated_car: CarImageCreate, db: Session = Depends(get_db)):
    get_car = db.query(CarImageModel).filter(CarImageModel.id == car_id).first()

    if not get_car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    for key, value in updated_car.model_dump().items():
        setattr(get_car, key, value)

    db.commit()
    db.refresh(get_car)
    return get_car

#@carimage.delete('/delete/{car_id}')
async def delete_car(car_id: int, db: Session = Depends(get_db)):
    remove_car = db.query(CarImageModel).filter(CarImageModel.id == car_id).first()

    if not remove_car:
        raise HTTPException(status_code=404, detail="Car not found")
        
    db.delete(remove_car)
    db.commit()
    db.refresh(remove_car)
    return remove_car