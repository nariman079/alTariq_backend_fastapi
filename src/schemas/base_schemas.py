from fastapi import HTTPException
from pydantic import BaseModel, validator


class UserCreate(BaseModel):
    title: str
    priority: int

