from fastapi import APIRouter, HTTPException
from starlette import status

from src.models.pairs import dto
from src.models.pairs.service import Service

transtypes_router = APIRouter()
service = Service()


@transtypes_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    tags=['Transaction types'],
    name='Create transaction type',
)
async def create(request: dto.PairView) -> dto.PairView:
    created_obj = await service.create(request)
    if created_obj is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot create transaction type'
        )
    else:
        return created_obj


@transtypes_router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Transaction types'],
    name='Read transaction type',
)
async def read(id: int) -> dto.PairView:
    read_obj = await service.read(id)
    if not read_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot read transaction type'
        )
    return read_obj


@transtypes_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['Transaction types'],
    name='Read all transaction types',
)
async def read_all() -> list[dto.PairView]:
    rows = await service.read_all()
    if rows is None:
        return []
    return rows


@transtypes_router.put(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Transaction types'],
    name='Update transaction type',
)
async def update(id: int, request: dto.PairView) -> dict:
    updated_bot = await service.update(id, request)
    if not updated_bot:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot update transaction type'
        )


@transtypes_router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Transaction types'],
    name='Delete transaction type',
)
async def delete(id: int) -> None:
    deleted_obj = await service.delete(id)
    if not deleted_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot delete transaction type'
        )
