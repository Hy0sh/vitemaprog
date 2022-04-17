from vitemaprog.models import User
from vitemaprog.requests import UserCreate, UserUpdate
import crypt

__all__ = ["UserController"]
class UserController():
    def get_users():
        return User.all()

    def get_user(user_uuid:str):
        return User.find(user_uuid, raise_exception=True)

    def create_user(user: UserCreate):
        user.password = crypt.crypt(user.password, crypt.mksalt(crypt.METHOD_SHA512))
        return User.create(user)

    def update_user(user_uuid: str, user: UserUpdate):
        userbdd = User.find(user_uuid, serialize=False, raise_exception=True)
        userbdd.update(user)

        return userbdd.to_json()

    def delete_user(user_uuid: str):
        user = User.find(user_uuid, serialize=False, raise_exception=True)
        user.delete()
