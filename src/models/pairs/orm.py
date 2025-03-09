from sqlalchemy import String, Column, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class Pair(Base):
    __tablename__ = 'pairs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    selected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, unique=False)
    qty_precision: Mapped[int] = mapped_column(Integer, nullable=False, unique=False)
