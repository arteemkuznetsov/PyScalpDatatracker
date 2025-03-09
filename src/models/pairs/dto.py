from src.models.dto import PydanticBaseModel


class PairView(PydanticBaseModel):
    id: int | None = None
    text: str
    selected: bool | None
    qty_precision: int
