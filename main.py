from fastapi import FastAPI
from app.api import api_router


application = FastAPI()
application.include_router(api_router)


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = False
#
#
# def fake_decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     return user
#
#
# @application.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user