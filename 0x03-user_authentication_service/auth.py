#!/usr/bin/python3
"""
Auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError, NoResultFound
import uuid


def _generate_uuid() -> str:
    """
    Generates a uuid
    :return: returns a generated uuid
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> str:
    """
    Hash a password
    :param password:
    :return: hashed password
    """
    to_encode = password.encode()
    return bcrypt.hashpw(to_encode, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        :param email: email of the user
        :param password: password of the user
        :return: new user object
        """
        try:
            user_exists = self._db.find_user_by(email=email)
            if user_exists:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        :param email: email of user
        :param password: password of user
        :return: True if account exists, else false
        """
        try:
            user_exists = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user_exists.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """

        :param email: email of the user
        :return: session id
        """
        try:
            user_exists = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user_exists.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        gets user from session_id
        :param session_id: session id of user
        :return: returns user object
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id):
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str)-> str:
        """
        generates a UUID and updates user's reset_token database field
        :param email: user's email
        :return: reset_token
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError("user doesn't exist")

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str)-> None:
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError()
        hashed_pwd = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_pwd, reset_token=None)





