from loguru import logger
from sqlalchemy import select, delete
from sqlalchemy.exc import DatabaseError

from src.models.repository import BaseRepository
from src.models.transtypes import dto, orm


class Repository(BaseRepository):
    database_model = orm.TransType
    view_model = dto.TransTypeView

    def __init__(self) -> None:
        super().__init__()
        self.base_stmt = self.__base_stmt()

    def __base_stmt(self):
        stmt = (
            select(self.database_model)
        )
        return stmt

    async def create(self, data: dto.TransTypeView) -> dto.TransTypeView:
        async with self.session() as session:
            async with session.begin():
                model = self._pydantic_to_model(data, self.database_model())
                session.add(model)
                await session.commit()
            await session.refresh(model)
            return self._model_to_pydantic(model, self.view_model)

    async def read(self, id: int) -> dto.TransTypeView | None:
        async with self.session() as session:
            stmt = (
                self.__base_stmt()
                .where(self.database_model.id == id)
            )
            model = (await session.scalars(stmt)).unique().first()
            if model:
                return self._model_to_pydantic(model, self.view_model)

    async def read_all(self) -> list[dto.TransTypeView]:
        stmt = (
            select(orm.TransType)
        )
        async with self.session() as session:
            try:
                result = (await session.scalars(stmt)).all()
                return [self._model_to_pydantic(sa_model, dto.TransTypeView) for sa_model in result]
            except DatabaseError as e:
                await session.rollback()
                logger.error(e)
                return []

    async def update(self, update_data: dto.TransTypeView, data: dto.TransTypeView) -> bool:
        async with self.session() as session:
            async with session.begin():
                model = self._pydantic_to_model(data, self.database_model())
                update_model = self._pydantic_to_model(update_data, model)
                await session.merge(update_model)
            await session.commit()
            return True

    async def delete(self, id: int) -> bool:
        stmt = (
            delete(orm.TransType)
            .where(orm.TransType.id == id)
            .returning(orm.TransType)
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
