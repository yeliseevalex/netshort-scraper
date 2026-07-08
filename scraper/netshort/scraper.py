import asyncio
import json
import math
import re

from scraper.core.config import (
    BASE_URL,
    RSC_TOKEN,
)
from scraper.core.client import HttpClient


async def fetch_page(client: HttpClient, page, semaphore):
    if page == 1:
        url = f"{BASE_URL}/drama/all-plots"
    else:
        url = f"{BASE_URL}/drama/all-plots/page/{page}"

    params = {
        "_rsc": RSC_TOKEN
    }

    async with semaphore:
        text = await client.get(url, params=params)

        if not text:
            print(f"Page {page}: пустой ответ")
            return []

        match = re.search(
            r'"videoList":(\[.*?\]),"totalCount":(\d+),"pageNum":(\d+),"pageSize":(\d+)',
            text,
            re.S
        )

        if not match:
            print(f"Page {page}: videoList not found")
            return []

        videos_json = match.group(1)

        videos = json.loads(videos_json)

        print(f"Page {page}: {len(videos)} of series")

        return videos



async def get_info(client: HttpClient):
    semaphore = asyncio.Semaphore(1)

    videos = await fetch_page(client, 1, semaphore)

    if not videos:
        raise Exception("Первая страница пустая")

    url = f"{BASE_URL}/drama/all-plots"

    text = await client.get(
        url,
        params={
            "_rsc": RSC_TOKEN
        }
    )

    if not text:
        raise Exception("Не удалось получить первую страницу")

    match = re.search(
        r'"totalCount":(\d+),"pageNum":(\d+),"pageSize":(\d+)',
        text
    )

    if not match:
        raise Exception("Не найдена информация пагинации")

    total = int(match.group(1))

    page_size = int(match.group(3))

    pages = math.ceil(total / page_size)

    return (
        videos,
        total,
        page_size,
        pages
    )