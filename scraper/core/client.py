import asyncio
import random
import aiohttp

from scraper.core.config import (
    HEADERS,
    MAX_RETRIES,
    REQUEST_TIMEOUT,
    MIN_DELAY,
    MAX_DELAY,
)
from scraper.core.proxy_manager import ProxyManager
from scraper.core.user_agent import UserAgentManager


class HttpClient:
    def __init__(self, session, proxy_manager=None, user_agent_manager=None):
        self.session = session

        self.proxy_manager = (proxy_manager or ProxyManager())

        self.user_agent_manager = (user_agent_manager or UserAgentManager())

    async def get(self, url, params=None, retries=MAX_RETRIES):
        for attempt in range(retries):
            try:
                proxy = self.proxy_manager.get_proxy()

                headers = HEADERS.copy()

                headers["user-agent"] = (self.user_agent_manager.get_user_agent())

                async with self.session.get(
                        url,
                        params=params,
                        headers=headers,
                        timeout=REQUEST_TIMEOUT,
                        proxy=proxy
                ) as response:


                    if response.status in [429, 500, 502, 503, 504]:
                        delay = 2 ** attempt

                        print(f"{url}: {response.status}, retry after {delay}s")

                        await asyncio.sleep(delay)

                        continue

                    response.raise_for_status()

                    text = await response.text()

                    await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

                    return text

            except Exception as e:
                print(f"HTTP error: {e}")

                await asyncio.sleep(2)

        return None