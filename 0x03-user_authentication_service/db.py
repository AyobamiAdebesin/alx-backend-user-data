#!/usr/bin/env python3
""" DB module """
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """ DB class """
    def __init__(self) -> None:
        """ Initialize a new DB instance """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Add a user to the database: No validation required """
        user_obj = User(email=email, hashed_password=hashed_password)
        self._session.add(user_obj)
        self._session.commit()
        return user_obj

    def find_user_by(self, **kwargs) -> User:
        """Finds a user based on a set of filters.
        """
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if result is None:
            raise NoResultFound()
        return result
    # def find_user_by(self, **kwargs) -> User:
    #     """ Find user in the database """
    #     # Verify that we receive valid arguments
    #     for k, v in kwargs.items():
    #         if k not in User.__dict__:
    #             raise InvalidRequestError
    #         # Check if the object is found in the database
    #         for user in self._session.query(User).all():
    #             if getattr(user, k) == v:
    #                 return user
    #     raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update user from in the database """
        all_users = self._session.query(User).all()

        # Get user by id
        for user in all_users:
            if user_id == user.id:
                user_obj = user
        # Set new attributes with kwargs
        for k, v in kwargs.items():
            if k not in User.__dict__:
                raise ValueError
            setattr(user_obj, k, v)
        self._session.add(user_obj)
        self._session.commit()
