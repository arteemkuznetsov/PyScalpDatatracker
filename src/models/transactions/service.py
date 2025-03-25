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
            type_id=request.type_id,
            order_id=request.order_id,
            quantity=request.quantity,
            fee=request.fee,
            pair_id=request.pair_id,
            balance=request.balance
        )
        return await self.repository.create(create_data)

    async def read(self, id: int) -> dto.TransactionView | None:
        return await self.repository.read(id)

    async def read_all(self) -> list[dto.TransactionView]:
        return await self.repository.read_all()

    async def read_order_ids(self) -> list[str]:
        return await self.repository.read_order_ids()

    async def read_since_timestamp(
            self,
            timestamp: int,
            type_id: int,
            include_previous: bool
    ) -> list[dto.TransactionView]:
        return await self.repository.read_since_timestamp(timestamp, type_id, include_previous)

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
