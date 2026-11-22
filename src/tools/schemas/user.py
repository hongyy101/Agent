from pydantic import BaseModel, Field

class UserOutput(BaseModel):
    user_id: int = Field(description="user_id")
    user_name: str = Field(description="user_name")
    email:str = Field(description="email")
    status:str = Field(description="status")
