import click
from flask.cli import with_appcontext
from flask import g, current_app
from datetime import datetime
from sqlalchemy import (
    create_engine,
    MetaData,
    Connection,
    Table,
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    DateTime,
)


DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/application"

engine = create_engine(DATABASE_URL)

metadata = MetaData()

posts = Table(
    "posts",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("title", String(50), unique=True, index=True),
    Column("body", Text()),
    Column("created_at", DateTime(), default=datetime.now),
    Column("updated_at", DateTime(), default=datetime.now, onupdate=datetime.now),
)

tags = Table(
    "tags",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("title", String(16), unique=True, index=True),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("name", Text(), index=True),
    Column("email", Text(), unique=True, index=True),
    Column("profile_pic", Text()),
)


def get_db() -> Connection:
    if "db" not in g:
        g.db = engine.connect()
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    metadata.create_all(bind=engine)


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
