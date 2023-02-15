#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User, Base
from sqlalchemy.exc import InvalidRequestError, NoResultFound
import bcrypt


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = \
            create_engine("mysql+mysqldb://root:410208olA$$$@localhost/a_db",
                          echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        if email and hashed_password:
            user = User(email=email, hashed_password=hashed_password)
            db = self._session
            db.add(user)
            db.commit()
            return user

    def find_user_by(self, **kwargs) -> User:
        if not kwargs:
            raise InvalidRequestError("Invalid")

        db = self._session

        user = db.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound("Not found")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:

        user = self.find_user_by(id=user_id)

        db = self._session
        for key, val in kwargs.items():
            if key not in ["id", "email", "hashed_password",
                           "session_id", "reset_token"]:
                raise ValueError("Invalid")
            setattr(user, key, val)
        db.add(user)
        db.commit()
        return None
