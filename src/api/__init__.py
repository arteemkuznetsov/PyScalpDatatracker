from fastapi import APIRouter

from src.api.pairs import pairs_router
from src.api.prices import prices_router
from src.api.transactions import transactions_router
from src.api.transtypes import transtypes_router

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(router=pairs_router, prefix='/pairs')
api_router.include_router(router=prices_router, prefix='/prices')
api_router.include_router(router=transactions_router, prefix='/transactions')
api_router.include_router(router=transtypes_router, prefix='/transtypes')
