import sqlalchemy
import databases
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ARRAY, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URI = os.getenv('DATABASE_URI')
# database = databases.Database(DATABASE_URI)
engine = sqlalchemy.create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()