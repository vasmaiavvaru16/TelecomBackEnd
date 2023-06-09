"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""
import uuid

from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_model"

    id = Column(String(36), primary_key=True, default=lambda _: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    mobile_number: Mapped[str] = mapped_column(String(128), nullable=False)
    postal_address: Mapped[str] = mapped_column(Text, nullable=False)
    active_plan_id: Mapped[str] = mapped_column(String(36), nullable=True)


class UserPlan(Base):
    __tablename__ = "user_plan"

    id = Column(String(36), primary_key=True, default=lambda _: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    plan_id = Column(String(36), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    active = Column(Boolean, nullable=False)
