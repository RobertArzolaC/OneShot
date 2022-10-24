import os

from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash

from src import create_app, db
from src.models import User


app = create_app()
cli = FlaskGroup(create_app=create_app)
DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD", "123456")


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    user = User(
        username="jsanchez",
        password=generate_password_hash(DEFAULT_PASSWORD),
        first_name="Jimy",
        last_name="Sanchez Aquije",
        alias="5131463",
        token="Fk#3#N,8",
    )
    db.session.add(user)
    db.session.commit()
    

if __name__ == "__main__":
    cli()
