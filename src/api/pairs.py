from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from src.auth import Auth
from src.models.pairs import dto
from src.models.pairs.service import Service

pairs_router = APIRouter()
service = Service()


@pairs_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    tags=['Trading pairs'],
    name='Create trading pair',
    dependencies=[Depends(Auth().check_access_token)]
)
async def create(request: dto.PairView) -> dto.PairView:
    created_obj = await service.create(request)
    if created_obj is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot create trading pair'
        )
    else:
        return created_obj


@pairs_router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Trading pairs'],
    name='Read trading pair'
)
async def read(id: int) -> dto.PairView:
    read_obj = await service.read(id)
    if not read_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot read trading pair'
        )
    return read_obj


@pairs_router.get(
    path='/selected/',
    status_code=status.HTTP_200_OK,
    tags=['Trading pairs'],
    name='Read all selected trading pairs'
)
async def read_selected() -> list[dto.PairView]:
    rows = await service.read_selected()
    if rows is None:
        return []
    return rows


@pairs_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['Trading pairs'],
    name='Read all trading pairs'
)
async def read_all() -> list[dto.PairView]:
    rows = await service.read_all()
    if rows is None:
        return []
    return rows


@pairs_router.put(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Trading pairs'],
    name='Update trading pair',
    dependencies=[Depends(Auth().check_access_token)]
)
async def update(id: int, request: dto.PairView) -> dict:
    updated_bot = await service.update(id, request)
    if not updated_bot:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot update trading pair'
        )


@pairs_router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Trading pairs'],
    name='Delete trading pair',
    dependencies=[Depends(Auth().check_access_token)]
)
async def delete(id: int) -> None:
    deleted_obj = await service.delete(id)
    if not deleted_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot delete trading pair'
        )
