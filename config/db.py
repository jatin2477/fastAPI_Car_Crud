from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQL_DB_URL = "mysql+pymysql://root@localhost:3306/fastapi"
SQL_DB_URL = "mysql+pymysql://jatin_wadhwani:deep70@radixusers2.com/jatin_wadhwani8"

engine = create_engine(SQL_DB_URL)

SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()        


