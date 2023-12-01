from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *


DATABASE_URL = "sqlite:///../data/workout_data.db"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(engine)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
