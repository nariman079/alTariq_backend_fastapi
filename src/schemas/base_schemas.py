from decimal import Decimal

from pydantic import BaseModel, EmailStr


class DisciplineBaseSchema(BaseModel):
    title: str
    priority: int
    description: str


class TeacherBaseSchema(BaseModel):
    telegram_id: str
    email: EmailStr
    name: str
    surname: str
    experience: int
    about: str
    opportunities: str
    study_methods: str
    price: Decimal
    gender: str


class DisciplineTeacherListSchema(BaseModel):
    id: int
    title: str


class TeacherListSchema(TeacherBaseSchema):
    id: int
    