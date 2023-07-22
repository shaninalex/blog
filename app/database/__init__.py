from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime


DATABASE_URL = 'postgresql+psycopg2://user:password@localhost:5432/application'

engine = create_engine(DATABASE_URL)

metadata = MetaData()

posts = Table('posts', metadata, 
    Column('id', Integer(), primary_key=True),
    Column('title', String(50), unique=True, index=True),
    Column('body', Text()),
    Column('created_at', DateTime(), default=datetime.now), 
    Column('updated_at', DateTime(), default=datetime.now, onupdate=datetime.now)
)

tags = Table('tags', metadata,
    Column('id', Integer(), primary_key=True),
    Column('title', String(16), unique=True, index=True)
)
