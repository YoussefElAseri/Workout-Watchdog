import datetime
import decimal

from typing import Optional, List

from sqlalchemy import Integer, String, Boolean, Date, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates


class Base(DeclarativeBase):
    pass


class Exercise(Base):
    __tablename__ = "exercise"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    body_weight: Mapped[bool] = mapped_column(Boolean, default=False)

    @validates("name")
    def validates_name(self, key, name):
        if len(name) > 50:
            raise Exception("Exercise name should be 50 characters or less!")
        return name


class Workout(Base):
    __tablename__ = "workout"

    workout_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.name"))
    date: Mapped[datetime.date] = mapped_column(Date)
    sets: Mapped[List["Set"]] = relationship("Set")


class Set(Base):
    __tablename__ = "set"

    set_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reps: Mapped[int] = mapped_column(Integer)
    weight: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    exercise_name: Mapped[str] = mapped_column(ForeignKey("exercise.name"))
    workout_id: Mapped[str] = mapped_column(ForeignKey("workout.workout_id"))

    @validates("reps")
    def validate_reps(self, key, reps):
        if reps <= 0:
            raise Exception("Number of reps should be at least one!")
        return reps

    @validates("weight")
    def validate_weight(self, key, weight):
        if weight <= 0:
            raise Exception("Weight should be higher than zero!")
        return weight

    def __repr__(self):
        if self.weight:
            return f"{self.exercise_name}       {self.reps}       {self.weight}kg"
        return f"{self.exercise_name}       {self.reps}"


class User(Base):
    __tablename__ = "user"

    name = mapped_column(String(30), primary_key=True)
    workouts: Mapped[List["Workout"]] = relationship()

    @validates("name")
    def validate_name(self, key, name):
        if len(name) > 30:
            raise Exception("User name should be 30 characters or less!")
        return name

    def __repr__(self):
        return self.name


class UserWeight(Base):
    __tablename__ = "user_weight"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(ForeignKey("user.name"))
    weight: Mapped[decimal] = mapped_column(DECIMAL)
    date: Mapped[datetime.date] = mapped_column(nullable=False)

    __table_args__ = (UniqueConstraint("user_name", "date", name="user_date_constraint"),)

    @validates("weight")
    def validate_weight(self, key, weight):
        if weight <= 30:
            raise Exception("Weight should be higher than 30!")
        return weight

    def __repr__(self):
        return f"{self.date} {self.weight:.2f}kg"
