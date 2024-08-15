#!/usr/bin/env python3
"""DB module
This module provides the DB class for managing database interactions using SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    This class handles the database connection and user management.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        This constructor sets up the database engine and creates the necessary tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        This property creates and returns a new session if one does not already exist.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database and return the User object.
        
        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.
        
        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments.
        
        Args:
            **kwargs: Arbitrary keyword arguments to filter the user query.
        
        Returns:
            User: The first User object matching the criteria.
        
        Raises:
            NoResultFound: If no user matches the criteria.
            InvalidRequestError: If invalid query arguments are provided.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found matching the criteria.")
        except Exception as e:
            raise InvalidRequestError("Invalid query arguments provided.") from e
