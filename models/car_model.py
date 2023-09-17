from sqlalchemy import Column, Integer, String, Boolean
from config.db import Base, engine

class CarModel(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    color = Column(String(50))
    price = Column(Integer)


Base.metadata.create_all(engine)    