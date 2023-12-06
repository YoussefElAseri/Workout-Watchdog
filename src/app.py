from datetime import date, datetime
from contextlib import contextmanager

import click
from sqlalchemy.exc import IntegrityError
from models import User, Set, Workout, Exercise, UserWeight
from database import Session


ADD_WORKOUT = 0
ADD_EXERCISE = 1
ADD_WEIGHT = 2
LOG_WORKOUT = 3
LOG_WEIGHT = 4
TODAY = 0
CUSTOM_DATE = 1


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    finally:
        session.close()


def get_binary_user_input():
    while True:
        choice = click.prompt("Choose your option", type=int)
        if choice in [0, 1]:
            return choice
        else:
            click.echo("Invalid choice. Please choose either 0 or 1!")


class App:
    def __init__(self):
        self.current_username = None

    def start(self):
        with Session() as session:
            users = session.query(User).all()
        if len(users) == 0:
            click.echo("Creating user")
            self.create_user()
        else:
            click.echo("0) Create User\n1) Login")
            choice = get_binary_user_input()
            if choice == 0:
                self.create_user()
            elif choice == 1:
                self.login()

    def create_user(self):
        while True:
            name = click.prompt("Enter your name", type=str)
            with get_session() as session:
                try:
                    new_user = User(name=name)
                    session.add(new_user)
                    session.commit()
                    click.echo("Successfully created account!")
                    self.current_username = name
                    self.menu()
                    break
                except IntegrityError as e:
                    session.rollback()
                    print(f"Failed to create user: {e}")
                except Exception as e:
                    session.rollback()
                    print(f"Something went wrong: {e}")

    def login(self):
        with get_session() as session:
            users = session.query(User).all()
            user_names = [user.name for user in users]
        for i in range(len(user_names)):
            click.echo(f"{i}) {user_names[i]}")
        while True:
            choice = click.prompt("Choose your option", type=int)
            if 0 <= choice < len(users):
                break
        self.current_username = user_names[choice]
        self.menu()

    def menu(self):
        # TODO: add delete functionality
        click.echo("0) Add new workout")
        click.echo("1) Add new exercise")
        click.echo("2) Add weight")
        click.echo("3) See workout history")
        click.echo("4) See weight history")
        while True:
            choice = click.prompt("Choose your option", type=int)
            if 0 <= choice <= 4:
                break
            else:
                click.echo("Choice should be a number from 0 to 4!")
        if choice == ADD_WORKOUT:
            self.add_workout()
        elif choice == ADD_EXERCISE:
            self.add_exercise()
        elif choice == ADD_WEIGHT:
            self.add_weight()
        elif choice == LOG_WORKOUT:
            self.print_workout_history()
        elif choice == LOG_WEIGHT:
            self.print_weight_history()
        else:
            raise Exception(f"Menu choice should be a number from 0 to 4 but is {choice}")

    def add_workout(self):
        workout_date: date
        sets: [Set] = []

        workout_date = self.ask_date("When did you work out?")
        with get_session() as session:
            workout = Workout(user_id=self.current_username, date=workout_date, sets=[])
            session.add(workout)
            session.commit()
            add_set = True
            while add_set:
                set_id = self.add_set(workout.workout_id)
                new_set = session.query(Set).filter(Set.set_id == set_id).first()
                sets.append(new_set)
                add_set = click.confirm("Add set?")
            workout.sets = sets
            current_user = session.query(User).filter(User.name == self.current_username).first()
            current_user.workouts.append(workout)
            session.commit()

    def ask_date(self, prompt) -> date:
        click.echo(prompt)
        click.echo("0) Today")
        click.echo("1) Custom date")

        choice = get_binary_user_input()
        if choice == TODAY:
            return date.today()

        new_date: date
        while True:
            date_str = click.prompt("Enter the date (DD-MM-YYYY)", type=str)
            try:
                new_date = datetime.strptime(date_str, "%d-%m-%Y").date()
                return new_date
            except ValueError:
                print("Invalid date format. Please enter the date in the format DD-MM-YYYY.")

    def add_set(self, workout_id1):
        with get_session() as session:
            exercises = session.query(Exercise).all()
            for i in range(len(exercises)):
                click.echo(f"{i}) {exercises[i].name}")

            while True:
                choice = click.prompt("Choose your option", type=int)
                if 0 <= choice < len(exercises):
                    break

            while True:
                reps = click.prompt("How many repetitions", type=int)
                if reps > 0:
                    break
                click.echo("Repetitions should be higher than 0!")

            new_set = Set(reps=reps, exercise_name=exercises[choice].name, workout_id=workout_id1)

            if not exercises[choice].body_weight:
                while True:
                    weight = click.prompt("How much weight", type=int)
                    if weight > 0:
                        break
                    click.echo("Weight should be higher than 0!")
                new_set.weight = weight

            session.add(new_set)
            session.commit()
            return new_set.set_id

    def add_exercise(self):
        exercise_name = click.prompt("Enter exercise name", type="str")
        bodyweight = click.confirm("Is it a bodyweight exercise?")
        with get_session() as session:
            exercise = Exercise(name=exercise_name, body_weight=bodyweight)
            session.add(exercise)
            session.commit()

    def add_weight(self):
        weigh_date = self.ask_date("When did you weigh yourself?")
        while True:
            weight = click.prompt("How much did you weigh", type=int)
            if weight > 30:
                break
            click.echo("Weight should be higher than 30!")

        with get_session() as session:
            session.add(UserWeight(user_name=self.current_username, weight=weight, date=weigh_date))
            session.commit()

    def print_workout_history(self):
        pass

    def print_weight_history(self):
        pass


@click.command()
def run():
    app = App()
    app.start()
