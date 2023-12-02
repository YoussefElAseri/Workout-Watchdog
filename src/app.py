from contextlib import contextmanager

import click
from sqlalchemy.exc import IntegrityError
from models import User, Set, Workout, Exercise
from database import Session


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


class App:
    def __init__(self):
        self.current_user = None

    def start(self):
        with Session() as session:
            users = session.query(User).all()
        if len(users) == 0:
            click.echo("Creating user")
            self.create_user()
        else:
            click.echo("0) Create User\n1) Login")
            while True:
                choice = click.prompt("Choose your option", type=int)
                if choice == 0:
                    self.create_user()
                    break
                elif choice == 1:
                    self.login()
                    break
                else:
                    click.echo("Choose either 0 or 1!")

    def create_user(self):
        while True:
            name = click.prompt("Enter your name", type=str)
            with get_session() as session:
                try:
                    new_user = User(name=name)
                    session.add(new_user)
                    session.commit()
                    click.echo("Successfully created account!")
                    self.current_user = new_user
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
        self.current_user = users[choice]
        self.menu()

    def menu(self):
        click.echo("0) Enter new workout")
        click.echo("1) Enter new exercise")
        click.echo("2) Enter weight")
        click.echo("3) See workout history")
        click.echo("4) See weight history")
        while True:
            choice = click.prompt("Choose your option", type=int)
            if 0 <= choice <= 4:
                break
        if choice == 0:
            self.add_workout()
        elif choice == 1:
            self.add_exercise()
        elif choice == 2:
            self.add_weight()
        elif choice == 3:
            self.print_workout_history()
        elif choice == 4:
            self.print_weight_history()
        else:
            raise Exception(f"Menu choice should be a number from 0 to 4 but is {choice}")

    def add_workout(self):
        pass

    def add_set(self):
        pass

    def add_exercise(self):
        pass

    def add_weight(self):
        pass

    def print_workout_history(self):
        pass

    def print_weight_history(self):
        pass


@click.command()
def run():
    app = App()
    app.start()
