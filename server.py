import uvicorn
from fastapi import FastAPI

from src.api import api_router


class Server(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs
            title="API Documentation",
            root_path="/docs",
            docs_url="/",
            openapi_url="/openapi.json",
            redoc_url=None
            )
        self.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run('server:Server', host='0.0.0.0', port=8000)
