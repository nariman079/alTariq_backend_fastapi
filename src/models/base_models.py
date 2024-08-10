from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, Float
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import relationship

from src.database import Base
from src.enums.type_enums import Gender

association_table = Table(
    'association',
    Base.metadata,
    Column(
        'teacher_id',
        ForeignKey('teachers.id'),
        primary_key=True
    ),
    Column(
        'discipline_id',
        ForeignKey('disciplines.id'),
        primary_key=True
    )
)


class Image(Base):
    """
    Модель изображения
    """
    __tablename__ = 'images'

    id = Column(
        Integer,
        primary_key=True
    )
    filename = Column(String)
    url = Column(String)
    teacher = relationship(
        "Teacher",
        back_populates='image'
    )


class Discipline(Base):
    """
    Модель дисциплины
    """
    __tablename__ = 'disciplines'

    id = Column(
        Integer,
        primary_key=True
    )
    title = Column(String)
    priority = Column(
        Integer,
        default=0
    )
    description = Column(String)
    teacher = relationship(
        "Teacher",
        secondary=association_table,
        back_populates="disciplines"
    )


class Teacher(Base):
    """
    Модель учителя
    """
    __tablename__ = "teachers"

    id = Column(
        Integer,
        primary_key=True
    )
    telegram_id = Column(
        String,
        unique=True
    )
    email = Column(
        String,
        unique=True
    )
    name = Column(String)
    surname = Column(String)
    experience = Column(Integer)
    about = Column(Text)
    opportunities = Column(Text)
    study_methods = Column(Text)
    price = Column(
        Float,
        default=0
    )
    gender = Column(
        PgEnum(
            Gender,
            name="teacher_gender"
        ),
        default=Gender.MALE
    )
    image_id = Column(
        Integer,
        ForeignKey('images.id'),
        unique=True
    )
    image = relationship(
        'Image',
        uselist=False,
        back_populates='teacher'
    )
    disciplines = relationship(
        "Discipline",
        secondary=association_table,
        back_populates="teacher"
    )
