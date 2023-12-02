"""User repository module"""
from typing import Optional, Union
from mongoengine import QuerySet, DoesNotExist
from bson import ObjectId

from app.infra.database.models.user import User as UserModel
from app.domain.user.entity import UserInDB, UserInCreate


class UserRepository:
    def __init__(self):
        pass

    def create(self, user: UserInCreate) -> UserInDB:
        """
        Create new user in db
        :param user:
        :return:
        """
        # create user document instance
        new_user = UserModel(**user.model_dump())
        # and save it to db
        new_user.save()

        return UserInDB.model_validate(new_user)

    def get_by_id(self, user_id: Union[str, ObjectId]) -> Optional[UserModel]:
        """
        Get user in db from id
        :param user_id:
        :return:
        """
        qs: QuerySet = UserModel.objects(id=user_id)
        # retrieve unique result
        # https://mongoengine-odm.readthedocs.io/guide/querying.html#retrieving-unique-results
        try:
            user: UserModel = qs.get()
            return user
        except DoesNotExist:
            return None

    def get_by_username(self, username: str) -> Optional[UserModel]:
        """
        :param username:
        :return:
        """
        qs: QuerySet = UserModel.objects(username=username)

        # retrieve unique result
        # https://mongoengine-odm.readthedocs.io/guide/querying.html#retrieving-unique-results
        try:
            user = qs.get()
        except DoesNotExist:
            return None
        return user

