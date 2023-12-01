import click
from models import User, Set, Workout, Exercise
from database import engine, Session


class App:
    def __init__(self):
        pass

    def start(self):
        with Session() as session:
            users = session.query(User).all()
            user_names = [user.name for user in users]
            if len(users) == 0:
                click.echo("creating user")
                self.create_user()
            else:
                click.echo("Choose your account:")
                for user_name in user_names:
                    click.echo(user_name)

    def create_user(self):
        pass


@click.command()
def run():
    app = App()
    app.start()
