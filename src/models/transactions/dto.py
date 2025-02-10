from src.models.dto import PydanticBaseModel


class TransactionView(PydanticBaseModel):
    value: float
    timestamp: int
    order_id: str | None = None  # TODO: исправить после того как заполню поля order_id в таблице и сделаю поле NOT_NULL
    type_id: int
