#!/usr/bin/env python3
"""DB module
This module provides the DB class for managing user data in a SQLite database using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import TypeVar

# List of valid fields for user queries and updates
VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """
    DB class.
    This class handles database operations related to user management, including adding,
    finding, and updating users.
    """

    def __init__(self):
        """
        Constructor.
        Initializes the database engine and creates the necessary tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """
        _session property.
        Returns a session object for interacting with the database. Creates a new session
        if one does not already exist.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        add_user method.
        Adds a new user to the database with the given email and hashed password.
        
        Args:
            email (str): The email address of the user.
            hashed_password (str): The hashed password of the user.
        
        Returns:
            User: The newly created User object, or None if input is invalid.
        """
        if not email or not hashed_password:
            return
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        find_user_by method.
        Searches for a user in the database based on the provided keyword arguments.
        
        Args:
            **kwargs: Arbitrary keyword arguments to filter the user query.
        
        Returns:
            User: The first User object matching the criteria.
        
        Raises:
            InvalidRequestError: If invalid query arguments are provided.
            NoResultFound: If no user matches the criteria.
        """
        if not kwargs or any(x not in VALID_FIELDS for x in kwargs):
            raise InvalidRequestError
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        update_user method.
        Updates the attributes of an existing user identified by user_id with the provided
        keyword arguments.
        
        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing the fields to update.
        
        Raises:
            ValueError: If any of the provided fields are invalid.
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k not in VALID_FIELDS:
                raise ValueError
            setattr(user, k, v)
        session.commit()
