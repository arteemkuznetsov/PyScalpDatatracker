from src.models.dto import PydanticBaseModel


class TransactionView(PydanticBaseModel):
    value: float
    timestamp: int
    type_id: int
