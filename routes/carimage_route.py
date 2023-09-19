from fastapi import APIRouter, Depends, HTTPException, UploadFile, Request
from sqlalchemy.orm import Session
from config.db import get_db
from models.carimage_model import CarImageModel
from schemas.carimage_schema import CarImageCreate, CarImageResponse
import os

carimage = APIRouter()

# Define the directory where you want to store the images
IMAGE_UPLOAD_DIR = "image_uploads"
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png"]
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

# Ensure the directory exists
os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)
    
@carimage.get('/{car_id}', response_model=CarImageResponse)
async def get_car(request: Request, car_id: int, db: Session =  Depends(get_db)):
    get_car = db.query(CarImageModel).filter(CarImageModel.id == car_id).first()
    if not get_car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    filename = get_car.image
    filepath = os.path.join(IMAGE_UPLOAD_DIR, filename)
    #Generate URLs relative to the current route
    #root_url = request.base_url
    get_car.image = f"{filepath}"
    return get_car


@carimage.post('/add/{car_id}', response_model=CarImageResponse)
async def add_car(request: Request, car_id: int,file: UploadFile,db: Session = Depends(get_db)):
    # validate file
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="File type not allowed. Please upload only JPG or PNG")

   # Read the file content and calculate its length
    file_content = await file.read()
    file_size = len(file_content)
    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File size exceeds the maximum allowed")

    # Generate a unique filename for the image
    filename = file.filename
    filepath = os.path.join(IMAGE_UPLOAD_DIR, filename)

    # Save the image to the server
    with open(filepath, "wb") as image_file:
        image_file.write(file.file.read())

    #Create a new ImageInfo instance with the filename and save it to the database
    car = CarImageModel(car_id=car_id, image=filepath, image_size="medium")
    db.add(car)
    db.commit()
    db.refresh(car)
    # Generate URLs relative to the current route
    #root_url = request.base_url
    filepath = os.path.join(filepath)
    car.image = f"{filepath}"
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