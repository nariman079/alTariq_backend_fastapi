import logging
from pathlib import Path

from fastapi import UploadFile, File
from starlette.requests import Request
import aiofiles


async def set_image_url(
        request: Request,
        filepath: str
):
    return str(request.base_url) + filepath


async def download_file(
        file: UploadFile = File(),
        path: Path | None = None
) -> dict[str, Path | None | UploadFile]:
    """ Скачивание файла в директорию """

    if not path:
        default_path = Path('uploads') / file.filename
    else:
        default_path = Path('uploads') / path / file.filename

    async with aiofiles.open(default_path, 'wb') as new_file:
        await new_file.write(await file.read())
    logging.info(msg=f"{default_path}")
    return {
        'file': file,
        'path': default_path
    }


async def define_extension(filename: str) -> str:
    return Path(filename).suffix
