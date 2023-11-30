from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from typing import List


Base = declarative_base()


class Set(Base):
    __tablename__ = "sets"

    set_id = Column(Integer, primary_key=True)
    reps = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=True)
    exercise_name = Column(String(50), ForeignKey("exercises.name"), nullable=False)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False, unique=True)
    workout = relationship("Workout", back_populates="sets")

    def __init__(self, reps, exercise_name, weight=None):
        self.reps = reps
        self.exercise_name = exercise_name
        if weight:
            self.weight = weight


class Exercise(Base):
    __tablename__ = "exercises"

    name = Column(String(50), primary_key=True)
    body_weight = Column(Boolean, nullable=False)

    def __init__(self, name, body_weight):
        self.name = name
        self.body_weight = body_weight


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    sets = relationship("Set", back_populates="workouts")

    def __init__(self, workout_date):
        self.date = workout_date


class User(Base):
    __tablename__ = "users"

    name: str = Column(String(30), primary_key=True)
    workouts = relationship("Workout", back_populates="user")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
