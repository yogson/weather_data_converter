import asyncio
from pathlib import Path
from typing import AsyncGenerator

import aiohttp
from aiohttp import ClientError

from exceptions import SourceLoadException
from receivers.utils import extract_urls_from_html
from settings import SOURCE_DIR
from utils.common import init_logger

logger = init_logger(__name__)


async def _download_file(session: aiohttp.ClientSession, url: str) -> Path | None:
    async with session.get(url) as response:
        if response.status == 200:
            try:
                content = await response.read()
                output_file = Path(SOURCE_DIR) / url.split("/")[-1]
                output_file.write_bytes(content)
                logger.info(f"Downloaded file: {output_file}")
            except (ClientError, IOError) as e:
                logger.error(e)
                return None
            return output_file

        logger.error(f"Failed to download from {url}: Status {response.status}")
        return None


async def receive(*args, source_url: str) -> AsyncGenerator[Path, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(source_url) as response:
            if response.status == 200:
                content = await response.text()
            else:
                raise SourceLoadException(response.status)
        tasks = []
        for file_name in extract_urls_from_html(content):
            full_url = source_url + file_name
            task = asyncio.create_task(_download_file(session, full_url))
            tasks.append(task)

        for download_task in asyncio.as_completed(tasks):
            file_path = await download_task
            if file_path:
                yield file_path
