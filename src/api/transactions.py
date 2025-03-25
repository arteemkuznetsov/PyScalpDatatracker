from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from src.auth import Auth
from src.models.transactions import dto
from src.models.transactions.service import Service

transactions_router = APIRouter()
service = Service()


@transactions_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    tags=['Transactions'],
    name='Create transaction',
    dependencies=[Depends(Auth().check_access_token)]
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
    path='/orderids/',
    status_code=status.HTTP_200_OK,
    tags=['Transactions'],
    name='Read all order IDs',
)
async def read_since_timestamp() -> list[str]:
    rows = await service.read_order_ids()
    if rows is None:
        return []
    return rows


@transactions_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['Transactions'],
    name='Read transactions since timestamp',
)
async def read_since_timestamp(
        timestamp: int,
        type_id: int,
        include_previous: bool = False
) -> list[dto.TransactionView]:
    rows = await service.read_since_timestamp(timestamp=timestamp, type_id=type_id, include_previous=include_previous)
    if rows is None:
        return []
    return rows


@transactions_router.put(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Transactions'],
    name='Update transaction',
    dependencies=[Depends(Auth().check_access_token)]
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
    dependencies=[Depends(Auth().check_access_token)]
)
async def delete(id: int) -> None:
    deleted_obj = await service.delete(id)
    if not deleted_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot delete transaction'
        )
