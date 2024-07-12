from fastapi import FastAPI

from src.routers.base_routers import base_router

app = FastAPI()


app.include_router(
    base_router,
    tags=['base'],
)