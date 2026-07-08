import asyncio
import aiohttp

from scraper.core.config import CONCURRENT_REQUESTS
from scraper.core.client import HttpClient
from scraper.core.exporter import save_csv
from scraper.netshort.scraper import fetch_page, get_info
from scraper.netshort.parser import parse_video
from scraper.core.proxy_manager import ProxyManager


async def main():
    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS)

    timeout = aiohttp.ClientTimeout(total=60)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        proxy_manager = ProxyManager(proxies=[])

        client = HttpClient(session, proxy_manager)

        first_page, total, page_size, pages = await get_info(client)

        print(f"\nTotal series: {total}\nPage size: {page_size}\nTotal pages: {pages}")

        all_videos = []

        all_videos.extend(first_page)

        semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

        tasks = [
            fetch_page(client, page, semaphore)
            for page in range(2, pages + 1)
        ]

        results = await asyncio.gather(*tasks)

        for result in results:
            all_videos.extend(result)


        print(f"Total collected: {len(all_videos)}")

        unique_videos = {}

        for video in all_videos:
            url = video.get("fullEpisodeNameUrl")

            if url:
                unique_videos[url] = video


        all_videos = list(unique_videos.values())

        print(f"After deduplication: {len(all_videos)}")

        data = [
            parse_video(video)
            for video in all_videos
        ]

        save_csv(data)

        print("Done!")



if __name__ == "__main__":
    asyncio.run(main())