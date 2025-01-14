from fastapi import APIRouter, HTTPException
from starlette import status

from src.models.transactions import dto
from src.models.transactions.service import Service

transactions_router = APIRouter()
service = Service()


@transactions_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    tags=['Transactions'],
    name='Create transaction',
)
async def create(request: dto.TransactionView) -> dto.TransactionView:
    created_obj = await service.create(request)
    if created_obj is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot create transaction'
        )
    else:
        return created_obj


# TODO: Read by TIMESTAMP field and by start-end
@transactions_router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Transactions'],
    name='Read transactions',
)
async def read(id: int) -> dto.TransactionView:
    read_obj = await service.read(id)
    if not read_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot read transaction'
        )
    return read_obj


@transactions_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['Transactions'],
    name='Read all transactions',
)
async def read_all() -> list[dto.TransactionView]:
    rows = await service.read_all()
    if rows is None:
        return []
    return rows


@transactions_router.put(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Transactions'],
    name='Update transaction',
)
async def update(id: int, request: dto.TransactionView) -> dict:
    updated_bot = await service.update(id, request)
    if not updated_bot:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot update transaction'
        )


@transactions_router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Transactions'],
    name='Delete transaction',
)
async def delete(id: int) -> None:
    deleted_obj = await service.delete(id)
    if not deleted_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot delete transaction'
        )
