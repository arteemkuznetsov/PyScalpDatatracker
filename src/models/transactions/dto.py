from src.models.dto import PydanticBaseModel


class TransactionView(PydanticBaseModel):
    value: float
    timestamp: int
    type_id: int
    order_id: str
    quantity: float
    fee: float
    pair_id: int
    balance: float
