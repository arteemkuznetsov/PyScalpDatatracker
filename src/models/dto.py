from pydantic import BaseModel


class PydanticBaseModel(BaseModel):
    class Config:
        from_attributes = True
