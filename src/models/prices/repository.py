import time

from loguru import logger
from sqlalchemy import select, delete
from sqlalchemy.exc import DatabaseError

from src.models.repository import BaseRepository
from src.models.prices import dto, orm
from src.models.pairs.service import Service as PriceService


class Repository(BaseRepository):
    database_model = orm.Price
    view_model = dto.PriceView

    def __init__(self) -> None:
        super().__init__()
        self.base_stmt = self.__base_stmt()

    def __base_stmt(self):
        stmt = (
            select(self.database_model)
        )
        return stmt

    async def create(self, data: dto.PriceView) -> dto.PriceView:
        async with self.session() as session:
            async with session.begin():
                model = self._pydantic_to_model(data, self.database_model())
                session.add(model)
                await session.commit()
            await session.refresh(model)
            return self._model_to_pydantic(model, self.view_model)

    async def read(self, id: int) -> dto.PriceView | None:
        async with self.session() as session:
            stmt = (
                self.__base_stmt()
                .where(self.database_model.id == id)
            )
            model = (await session.scalars(stmt)).unique().first()
            if model:
                return self._model_to_pydantic(model, self.view_model)

    async def read_current_pair_from_time(self, diff_sec: int) -> list[dto.PriceView] | None:
        pair_service = PriceService()
        selected_pair = await pair_service.read_selected()
        if not selected_pair:
            return []

        stmt = (
            select(orm.Price)
            .where(self.database_model.timestamp >= int(time.time()) - diff_sec)
            .where(self.database_model.pair_id == selected_pair.id)
        )
        async with self.session() as session:
            try:
                result = (await session.scalars(stmt)).all()
                return [self._model_to_pydantic(sa_model, dto.PriceView) for sa_model in result]
            except DatabaseError as e:
                await session.rollback()
                logger.error(e)
                return []

    async def read_all(self) -> list[dto.PriceView]:
        stmt = (
            select(orm.Price)
        )
        async with self.session() as session:
            try:
                result = (await session.scalars(stmt)).all()
                return [self._model_to_pydantic(sa_model, dto.PriceView) for sa_model in result]
            except DatabaseError as e:
                await session.rollback()
                logger.error(e)
                return []

    async def update(self, update_data: dto.PriceView, data: dto.PriceView) -> bool:
        async with self.session() as session:
            async with session.begin():
                model = self._pydantic_to_model(data, self.database_model())
                update_model = self._pydantic_to_model(update_data, model)
                await session.merge(update_model)
            await session.commit()
            return True

    async def delete(self, id: int) -> bool:
        stmt = (
            delete(orm.Price)
            .where(orm.Price.id == id)
            .returning(orm.Price)
        )
        async with self.session() as session:
            try:
                await session.scalars(stmt)
                await session.commit()
                return True
            except DatabaseError as e:
                await session.rollback()
                logger.error(e)
                return False
