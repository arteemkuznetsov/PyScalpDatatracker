from sqlalchemy import BigInteger, ForeignKey, Column, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[float] = mapped_column(Numeric(precision=10, scale=4), nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pair_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('pairs.id', ondelete='CASCADE'), nullable=False)
    pair = relationship(
        'Pair',
        foreign_keys=[pair_id],
        lazy='joined',
    )
