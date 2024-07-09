from fastapi import HTTPException
from pydantic import BaseModel, validator


class UserCreate(BaseModel):
    title: str
    priority: int

    @validator("title")
    def validate_username(cls, value):
        if len(value) <= 4:
            raise HTTPException(
                status_code=422,
                detail="Minimal len username is 4 symbols"
            )
        return value