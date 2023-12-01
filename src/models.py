import datetime
import decimal

from typing import Optional, List

from sqlalchemy import Integer, String, Boolean, Date, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Exercise(Base):
    __tablename__ = "exercise"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    body_weight: Mapped[bool] = mapped_column(Boolean)


class Set(Base):
    __tablename__ = "set"

    set_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reps: Mapped[int] = mapped_column(Integer)
    weight: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    exercise_name: Mapped[str] = mapped_column(ForeignKey("exercise.name"))
    workout_id: Mapped[int] = mapped_column(ForeignKey("workout.workout_id"))


class Workout(Base):
    __tablename__ = "workout"

    workout_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.name"))
    date: Mapped[datetime.date] = mapped_column(Date)
    sets: Mapped[List["Set"]] = relationship()


class User(Base):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(String(30), primary_key=True)
    workouts: Mapped[List["Workout"]] = relationship()

    def __repr__(self):
        return self.name


class UserWeight(Base):
    __tablename__ = "user_weight"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(ForeignKey("user.name"))
    weight: Mapped[decimal] = mapped_column(DECIMAL)
    date: Mapped[datetime.date] = mapped_column(nullable=False)

    __table_args__ = (UniqueConstraint("user_name", "date", name="user_date_constraint"),)
