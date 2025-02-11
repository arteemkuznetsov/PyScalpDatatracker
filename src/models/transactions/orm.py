from sqlalchemy import BigInteger, ForeignKey, Column, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[float] = mapped_column(Numeric(precision=10, scale=4), nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False)
    order_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    type_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('transtypes.id', ondelete='CASCADE'), nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(precision=12, scale=6), nullable=False)
    fee: Mapped[float] = mapped_column(Numeric(precision=18, scale=12), nullable=False)
    pair_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('pairs.id', ondelete='CASCADE'), nullable=False)
    type = relationship(
        'TransType',
        foreign_keys=[type_id],
        lazy='joined',
    )
    pair = relationship(
        'Pair',
        foreign_keys=[pair_id],
        lazy='joined'
    )
