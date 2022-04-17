from fastapi import APIRouter, status
from vitemaprog.controllers import UserController
from vitemaprog.requests import UserCreate, UserUpdate, UserOut


api_router = APIRouter()


@api_router.get('/users', response_model=list[UserOut], tags=['users'], status_code=status.HTTP_200_OK)
async def get_users():
    return UserController.get_users()

@api_router.post('/users', response_model=UserOut, tags=['users'], status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return UserController.create_user(user)

@api_router.get('/users/{user_uuid}', response_model=UserOut, tags=['users'], status_code=status.HTTP_200_OK)
async def get_user(user_uuid: str):
    return UserController.get_user(user_uuid)

@api_router.put('/users/{user_uuid}', response_model=UserOut, tags=['users'], status_code=status.HTTP_200_OK)
async def update_user(user_uuid: str, user: UserUpdate):
    return UserController.update_user(user_uuid, user)

@api_router.delete('/users/{user_uuid}', response_model=None, tags=['users'], status_code=status.HTTP_204_NO_CONTENT)
async def get_users(user_uuid: str):
    UserController.delete_user(user_uuid)
