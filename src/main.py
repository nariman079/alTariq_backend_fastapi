import logging
import time

from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles

from src.routers.admin_routers import base_router

logging.basicConfig(
    filename="setup.log",
    level=logging.INFO,
)

app = FastAPI()


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(
    base_router,
    tags=['base'],
)
app.mount(
    '/uploads',
    StaticFiles(
        directory='uploads'
    ),
    name='uploads'
)
