from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class TransType(Base):
    __tablename__ = 'transtypes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String, nullable=False, unique=True)
