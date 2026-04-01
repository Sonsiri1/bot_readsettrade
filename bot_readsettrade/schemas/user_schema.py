from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    username: str
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

# class UserResponse(BaseModel):
#     id: int
#     username: str

#     class Config:
#         from_attributes = True