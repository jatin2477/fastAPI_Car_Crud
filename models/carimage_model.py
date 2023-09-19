from sqlalchemy import Column, Integer, ForeignKey, LargeBinary, String
from sqlalchemy.orm import relationship
from config.db import Base, engine

class CarImageModel(Base):
    __tablename__ = "car_image"

    id = Column(Integer, primary_key=True)
    #image = Column(LargeBinary)
    image = Column(String(255))
    car_id = Column(Integer, ForeignKey("car.id"))
    image_size = Column(String(50))

    car = relationship("CarModel", back_populates="image")

Base.metadata.create_all(engine)