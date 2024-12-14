from typing import Optional

from pydantic import BaseModel, Field


class UserProfileCreate(BaseModel):
    full_name: str = Field(..., max_length=150)
    age: int = Field(..., ge=0, le=120)
    gender: str = Field(..., max_length=20)
    marital_status: str = Field(..., max_length=20)
    occupation: str = Field(..., max_length=100)


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=150)
    age: Optional[int] = Field(None, ge=0, le=120)
    gender: Optional[str] = Field(None, max_length=20)
    marital_status: Optional[str] = Field(None, max_length=20)
    occupation: Optional[str] = Field(None, max_length=100)

    class Config:
        from_attributes = True
