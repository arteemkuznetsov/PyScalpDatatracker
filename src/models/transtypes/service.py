from src.models.transtypes import dto
from src.models.transtypes.repository import Repository


class Service:
    def __init__(
            self
    ) -> None:
        self.repository = Repository()

    async def create(self, request: dto.TransTypeView) -> dto.TransTypeView:
        create_data = dto.TransTypeView(text=request.text)
        return await self.repository.create(create_data)

    async def read(self, id: int | None = None, text: str | None = None) -> dto.TransTypeView | None:
        return await self.repository.read(id, text)

    async def read_all(self) -> list[dto.TransTypeView]:
        return await self.repository.read_all()

    async def update(self, id: int, request: dto.TransTypeView) -> bool:
        data = await self.repository.read(id=id)
        if not data:
            return False
        update_data = dto.TransTypeView(text=request.text)
        return await self.repository.update(update_data, data)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)
