from src.models.dto import PydanticBaseModel


class TransactionView(PydanticBaseModel):
    value: float
    timestamp: int
    order_id: str
    type_id: int
