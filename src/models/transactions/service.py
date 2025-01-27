from src.models.transactions import dto
from src.models.transactions.repository import Repository


class Service:
    def __init__(
            self
    ) -> None:
        self.repository = Repository()

    async def create(self, request: dto.TransactionView) -> dto.TransactionView:
        create_data = dto.TransactionView(
            value=request.value,
            timestamp=request.timestamp,
            type_id=request.type_id
        )
        from loguru import logger
        logger.info('INSIDE Service.create() transaction:', create_data)
        return await self.repository.create(create_data)

    async def read(self, id: int) -> dto.TransactionView | None:
        return await self.repository.read(id)

    async def read_all(self) -> list[dto.TransactionView]:
        return await self.repository.read_all()

    async def update(self, id: int, request: dto.TransactionView) -> bool:
        data = await self.repository.read(id=id)
        if not data:
            return False
        update_data = dto.TransactionView(
            value=request.value,
            timestamp=request.timestamp,
            type_id=request.type_id
        )
        return await self.repository.update(update_data, data)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)
