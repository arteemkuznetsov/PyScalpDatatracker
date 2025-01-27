from sqlalchemy import BigInteger, ForeignKey, Column, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[float] = mapped_column(Numeric(precision=10, scale=4), nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False)
    type_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('transtypes.id', ondelete='CASCADE'), nullable=False)
    type = relationship(
        'TransType',
        foreign_keys=[type_id],
        lazy='joined',
    )
