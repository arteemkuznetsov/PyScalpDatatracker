from src.models.dto import PydanticBaseModel


class PriceView(PydanticBaseModel):
    value: float
    timestamp: int
    pair_id: int
