from itertools import cycle


class ProxyManager:
    def __init__(self, proxies=None):
        self.proxies = proxies or []
        self.proxy_pool = (cycle(self.proxies) if self.proxies else None)

    def get_proxy(self):
        if not self.proxy_pool:
            return None

        return next(self.proxy_pool)