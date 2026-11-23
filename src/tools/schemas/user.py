from pydantic import BaseModel, Field
from typing import Literal

class UserInput(BaseModel):
    user_id:int = Field(description="user_id")
    detail_level:Literal["full","basic"] = Field(default="basic", description="detail_level")


class SimpleUserOutput(BaseModel):
    user_id: int = Field(description="user_id")
    user_name: str = Field(description="user_name")
    email:str = Field(description="email")
    status:str = Field(description="status")


class FullUserOutput(BaseModel):
    user_id: int = Field(description="user_id")
    user_name: str = Field(description="user_name")
    email:str = Field(description="email")
    status:str = Field(description="status")
    age:int = Field(description="age")
    gender:str = Field(description="gender")