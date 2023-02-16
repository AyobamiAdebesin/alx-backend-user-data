#!/usr/bin/env python3
""" Mode for a user class """
from sqlalchemy import Column, String, Integer, String, Metadata
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

my_metadata = Metadata()
Base = declarative_base(metadata=my_metadata)


class User(Base):
    """ User class that represents the user table """
    __tablename__ = 'users'
    id = Column(Integer(), unique=True, nullable=False, primary_key=True)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(256), nullable=False)
    session_id = Column(String(256), nullable=True)
    reset_token = Column(String(256), nullable=True)
