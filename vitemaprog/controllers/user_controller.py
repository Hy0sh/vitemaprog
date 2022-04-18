from vitemaprog.exeptions.validation_exception import ValidationException
from vitemaprog.models import UserModel
from vitemaprog.requests import UserCreate, UserUpdate, UserUpdatePassword


__all__ = ["UserController"]
class UserController():
    def get_users():
        return UserModel.all()

    def get_user(user_uuid:str):
        return UserModel.find(user_uuid, raise_exception=True)

    def create_user(user: UserCreate):
        user.password = UserModel.hash_password(user.password)
        return UserModel.create(user).to_json()

    def update_user(user_uuid: str, user: UserUpdate):
        user_model = UserModel.find(user_uuid, serialize=False, raise_exception=True)
        user_model.update(user)

        return user_model.to_json()

    def update_user_password(user_uuid: str, user: UserUpdatePassword):
        user_model = UserModel.find(user_uuid, serialize=False, raise_exception=True)

        if not user_model.validate_password(user.current_password):
            raise ValidationException(message="Current password is incorrect", field="current_password",type="value_error.password_invalid")

        user_model.password = UserModel.hash_password(user.new_password)
        user_model.save()

        return user_model.to_json()

    def delete_user(user_uuid: str):
        user_model = UserModel.find(user_uuid, serialize=False, raise_exception=True)
        user_model.delete()
