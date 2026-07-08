BASE_URL = "https://netshort.com"

HEADERS = {
    "accept": "*/*",
    "accept-language": "uk,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "next-url": "/en/drama/all-plots",
    "rsc": "1",
    "referer": "https://netshort.com/drama/all-plots",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/149 Safari/537.36"
    ),
}

RSC_TOKEN = "9vwgx"

MAX_RETRIES = 3

REQUEST_TIMEOUT = 30

CONCURRENT_REQUESTS = 10

MIN_DELAY = 0.2

MAX_DELAY = 0.6