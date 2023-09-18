from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base, engine

class CarModel(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    color = Column(String(50))
    price = Column(Integer)
    # car_company = Column(String(50))

    image = relationship("CarImageModel", back_populates="car")

Base.metadata.create_all(engine)