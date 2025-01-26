from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from src.auth import Auth
from src.models.transtypes import dto
from src.models.transtypes.service import Service

transtypes_router = APIRouter()
service = Service()


@transtypes_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    tags=['Transaction types'],
    name='Create transaction type',
    dependencies=[Depends(Auth().check_access_token)]
)
async def create(request: dto.TransTypeView) -> dto.TransTypeView:
    created_obj = await service.create(request)
    if created_obj is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot create transaction type'
        )
    else:
        return created_obj


@transtypes_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['Transaction types'],
    name='Read transaction type',
)
async def read(id: int | None = None, text: str | None = None) -> dto.TransTypeView:
    read_obj = await service.read(id, text)
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
async def read_all() -> list[dto.TransTypeView]:
    rows = await service.read_all()
    if rows is None:
        return []
    return rows


@transtypes_router.put(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Transaction types'],
    name='Update transaction type',
    dependencies=[Depends(Auth().check_access_token)]
)
async def update(id: int, request: dto.TransTypeView) -> dict:
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
    dependencies=[Depends(Auth().check_access_token)]
)
async def delete(id: int) -> None:
    deleted_obj = await service.delete(id)
    if not deleted_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot delete transaction type'
        )
