from datetime import datetime
from typing import List
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Employee(Base):
    "Модель сотрудника"

    __tablename__ = "employees"
    
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    telegram_id: Mapped[int] = mapped_column(unique=True)
    date_registered: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now()
    )
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_banned: Mapped[bool] = mapped_column(default=False)
    cheques: Mapped[List['Cheque']] = relationship(lazy='selectin')


class Buyer(Base):
    "Модель клиента (покупателя)"

    __tablename__ = "buyers"
    
    name: Mapped[str] = mapped_column(String(30))
    number: Mapped[str] = mapped_column(String(11), unique=True)
    date_registered: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now()
    )
    bonus_points: Mapped[int] = mapped_column(default=0)
    count_aplications: Mapped[int] = mapped_column(default=0)
    cheques: Mapped[List['Cheque']] = relationship(lazy='selectin')


class BonusPoint(Base):
    "Модель бонусов"
    
    __tablename__ = 'bonus_point'

    name: Mapped[str] = mapped_column(String(30), unique=True)
    percent: Mapped[int] = mapped_column(default=10)


class Cheque(Base):
    """Модель чеков"""

    __tablename__ = 'cheques'
    amount: Mapped[int] = mapped_column()
    films: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now()
    )
    employee: Mapped[int] = mapped_column(ForeignKey("employees.telegram_id"))
    buyer: Mapped[int] = mapped_column(ForeignKey("buyers.id"))


