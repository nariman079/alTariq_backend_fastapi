from decimal import Decimal
from typing import List

from pydantic import BaseModel, EmailStr

from src.enums.type_enums import Gender


class CreateDisciplineSchema(BaseModel):
    title: str
    priority: int


class CreateTeacherSchema(BaseModel):
    telegram_id: str | None = None
    email: EmailStr
    name: str
    surname: str
    about: str
    opportunities: str
    study_methods: str
    price: Decimal
    gender: Gender
    image: bytes | None = None
    disciplines_id: List[int]


class ListDisciplineSchema(BaseModel):
    id: int
    title: str


class ListTeacherSchema(BaseModel):
    id: int
    name: str
    surname: str
    price: Decimal
    image_url: str
    disciplines_title: List[str]
    lesson_count: int
    experience: int


class DetailTeacherSchema(BaseModel):
    name: str
    surname: str
    about: str
    opportunities: str
    study_methods: str
    price: Decimal
    gender: Gender
    image_url: bytes
    disciplines_id: List[int]
    lesson_count: int
    experience: int
