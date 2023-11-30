from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///data/workout_data.db"

engine = create_engine(DATABASE_URL, echo=True)
