from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from src.auth import Auth
from src.models.prices import dto
from src.models.prices.service import Service

prices_router = APIRouter()
service = Service()


@prices_router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    tags=['Prices'],
    name='Create price',
    dependencies=[Depends(Auth().check_access_token)]
)
async def create(request: dto.PriceView) -> dto.PriceView:
    created_obj = await service.create(request)
    if created_obj is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot create price'
        )
    else:
        return created_obj


@prices_router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Prices'],
    name='Read price',
)
async def read(id: int) -> dto.PriceView:
    read_obj = await service.read(id)
    if not read_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot read price'
        )
    return read_obj


@prices_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['Prices'],
    name='Read multiple prices: All / Selected Pair Observations Since N Seconds Ago',
)
async def read_all(diff_sec: int | None = None) -> list[dto.PriceView]:
    if diff_sec:
        rows = await service.read_current_pair_from_time(diff_sec)
    else:
        rows = await service.read_all()
    if rows is None:
        return []
    return rows


@prices_router.put(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Prices'],
    name='Update price',
    dependencies=[Depends(Auth().check_access_token)]
)
async def update(id: int, request: dto.PriceView) -> dict:
    updated_bot = await service.update(id, request)
    if not updated_bot:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot update price'
        )


@prices_router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Prices'],
    name='Delete price',
    dependencies=[Depends(Auth().check_access_token)]
)
async def delete(id: int) -> None:
    deleted_obj = await service.delete(id)
    if not deleted_obj:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Cannot delete price'
        )
