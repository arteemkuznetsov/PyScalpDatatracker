from src.models.prices import dto
from src.models.prices.repository import Repository


class Service:
    def __init__(
            self
    ) -> None:
        self.repository = Repository()

    async def create(self, request: dto.PriceView) -> dto.PriceView:
        create_data = dto.PriceView(
            value=request.value,
            timestamp=request.timestamp,
            pair_id=request.pair_id
        )
        return await self.repository.create(create_data)

    async def read(self, id: int) -> dto.PriceView | None:
        return await self.repository.read(id)

    async def read_last_sec_cur_pair(self, diff_sec: int) -> list[dto.PriceView] | None:
        return await self.repository.read_last_sec_cur_pair(diff_sec)

    async def read_all(self) -> list[dto.PriceView]:
        return await self.repository.read_all()

    async def update(self, id: int, request: dto.PriceView) -> bool:
        data = await self.repository.read(id=id)
        if not data:
            return False
        update_data = dto.PriceView(
            value=request.value,
            timestamp=request.timestamp,
            pair_id=request.pair_id
        )
        return await self.repository.update(update_data, data)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)
