from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, PlainSerializer

from src.enums.type_enums import Gender


class DisciplineBaseSchema(BaseModel):
    title: str
    priority: int
    description: str


class TeacherBaseSchema(BaseModel):
    telegram_id: Annotated[str, Field(..., description="The unique Telegram ID of the teacher")]
    email: Annotated[EmailStr, Field(..., description="The teacher's email address")]
    name: Annotated[str, Field(..., description="The teacher's first name")]
    surname: Annotated[str, Field(..., description="The teacher's surname")]
    experience: Annotated[int, Field(..., description="Years of teaching experience", ge=0)]
    about: Annotated[str, Field(..., description="A brief description about the teacher")]
    opportunities: Annotated[str, Field(..., description="The opportunities offered by the teacher")]
    study_methods: Annotated[str, Field(..., description="Study methods used by the teacher")]
    price: Annotated[float, Field()]
    gender: Annotated[Gender, Field()]

    class Config:
        orm_mode = True

class TeacherUpdateSchema(BaseModel):
    telegram_id: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    experience: Optional[int] = None
    about: Optional[str] = None
    opportunities: Optional[str] = None
    study_methods: Optional[str] = None
    price: Optional[float] = None
    gender: Optional[Gender] = None

    class Config:
        orm_mode = True


class DisciplineTeacherListSchema(BaseModel):
    id: int
    title: str


class TeacherListSchema(BaseModel):
    id: int
    name: Annotated[str, Field(..., description="The teacher's first name")]
    surname: Annotated[str, Field(..., description="The teacher's surname")]
    experience: Annotated[int, Field(..., description="Years of teaching experience", ge=0)]
    discipline: Annotated[list, DisciplineTeacherListSchema]
    discipline_count: Annotated[int, Field()]