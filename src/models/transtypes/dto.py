from src.models.dto import PydanticBaseModel


class TransTypeView(PydanticBaseModel):
    id: int
    text: str
