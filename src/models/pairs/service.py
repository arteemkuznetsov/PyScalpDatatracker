from src.models.pairs import dto
from src.models.pairs.repository import Repository


class Service:
    def __init__(
            self
    ) -> None:
        self.repository = Repository()

    async def create(self, request: dto.PairView) -> dto.PairView:
        create_data = dto.PairView(text=request.text, selected=request.selected)
        return await self.repository.create(create_data)

    async def read(self, id: int) -> dto.PairView | None:
        return await self.repository.read(id)

    async def read_selected(self) -> list[dto.PairView] | None:
        return await self.repository.read_selected()

    async def read_all(self) -> list[dto.PairView]:
        return await self.repository.read_all()

    async def update(self, id: int, request: dto.PairView) -> bool:
        data = await self.repository.read(id=id)
        if not data:
            return False
        update_data = dto.PairView(text=request.text, selected=request.selected)
        return await self.repository.update(update_data, data)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)
