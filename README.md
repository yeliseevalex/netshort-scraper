# NetShort Series Scraper

A scalable asynchronous scraper for collecting publicly available series data from NetShort.com.

The scraper collects publicly available series information and exports the data into a clean CSV file.

## Collected Data

The scraper extracts the following fields:

- Series title
- Series URL
- Cover image URL
- Description
- Genre / category
- Number of episodes
- Status (if available)
- Tags / ranking (if available)

The output is stored as:

```
output/series.csv
```

---

# Approach and Technology Choice

## Initial Investigation

The first step was to analyze how NetShort loads its data.

I started by looking for public API endpoints that could provide the required series information.

After opening the browser developer tools, the website triggered a debugging protection mechanism, which was disabled before continuing the analysis.

I inspected the network requests made when opening:

```
https://netshort.com/drama/all-plots
```

During this process, I found that the page was using a Next.js Server Components response (RSC).

The RSC response contained the required series information, including:

- title
- cover image
- description
- episode count
- genre information
- pagination metadata

Instead of using browser automation, I extracted the RSC request details and reproduced the request using a regular HTTP client.

The response was then parsed to extract the required data.

---

# Why I chose asynchronous HTTP requests

Several scraping approaches were considered:

## Selenium / Playwright

Pros:

- Can execute JavaScript
- Works with dynamic websites

Cons:

- Higher resource usage
- Slower execution
- Requires browser management

For this project, browser automation was unnecessary because the required data was already available through the public RSC response.

---

## Scrapy

Pros:

- Excellent crawling framework
- Good for very large scraping projects
- Built-in pipelines and middlewares

Cons:

- More overhead for this specific task
- The website did not require complex crawling logic

Since NetShort exposes all required information through predictable paginated requests and the total number of pages is relatively small, Scrapy would introduce unnecessary complexity.

---

## aiohttp asynchronous requests

The final choice was:

```
Python + aiohttp
```

Reasons:

- High performance through concurrent requests
- Lightweight compared to browser automation
- Perfect fit for paginated HTTP-based scraping
- Easy integration with retries, proxies and request management

---

# Architecture

The project was designed as a reusable scraping system rather than a single script.

Current architecture:

```
netshort_scraper/

├── main.py

├── scraper/
│
│   ├── core/
│   │   ├── client.py
│   │   ├── config.py
│   │   ├── exporter.py
│   │   ├── models.py
│   │   ├── proxy_manager.py
│   │   └── user_agent.py
│   │
│   └── netshort/
│       ├── scraper.py
│       └── parser.py

└── output/
    └── series.csv
```

The structure separates:

- HTTP communication
- proxy handling
- parsing logic
- data models
- exporting
- website-specific scraping logic

This allows additional scrapers to be added without changing the core infrastructure.

---

# Core Components

## HttpClient

Location:

```
scraper/core/client.py
```

Responsible for all HTTP communication.

Features:

- Centralized request handling
- Retry mechanism
- Timeout management
- Random delays between requests
- Proxy support
- User-Agent rotation

The scraper logic never communicates directly with `aiohttp`. All requests go through this client.

Example flow:

```
NetShort scraper -> HttpClient -> aiohttp request
```

---

## ProxyManager

Location:

```
scraper/core/proxy_manager.py
```

Responsible for proxy management.

Currently implemented as a separate component to allow easy integration with proxy providers such as:

- residential proxies
- datacenter proxies
- external proxy APIs

The scraper can rotate proxies without changing site-specific scraping code.

Example:

```
HttpClient -> ProxyManager -> Selected proxy
```

---

## UserAgentManager

Location:

```
scraper/core/user_agent.py
```

Provides User-Agent rotation.

Instead of sending every request with the same browser fingerprint, the client can select different User-Agent values.

This component is separated so it can later be extended with more advanced browser fingerprinting strategies.

---

## Series dataclass

Location:

```
scraper/core/models.py
```

Defines the common data model.

Example:

```python
Series(
    title="Example",
    url="https://...",
    cover_image="https://...",
    description="...",
    genre="Drama",
    episodes=50,
    status=None,
    tags=None
)
```

Using a data model instead of raw dictionaries makes the system easier to extend and maintain.

---

## NetShort Parser

Location:

```
scraper/netshort/parser.py
```

Responsible only for converting raw NetShort JSON/RSC data into structured `Series` objects.

It does not handle:

- HTTP requests
- CSV export
- pagination

---

## NetShort Scraper

Location:

```
scraper/netshort/scraper.py
```

Responsible for:

- pagination handling
- downloading NetShort pages
- extracting the series list from RSC responses

It uses `HttpClient` instead of making direct HTTP requests.

---

## CSV Exporter

Location:

```
scraper/core/exporter.py
```

Responsible only for exporting collected data into CSV format.

The exporter is independent from NetShort, so it can be reused for future scrapers.

---

# Anti-Bot and Reliability Features

The scraper includes several reliability mechanisms:

## Retry handling

Retries are performed for temporary errors:

```
429
500
502
503
504
```

with exponential backoff delays.

Example:

```
Attempt 1 -> wait 1 second
Attempt 2 -> wait 2 seconds
Attempt 3 -> wait 4 seconds
```

---

## Request delays

Random delays are added between requests to avoid generating an unnatural request pattern.

---

## Timeout handling

All requests have configurable timeouts.

---

## Proxy-ready architecture

Proxy rotation is implemented as a separate service and can be enabled without modifying the scraper itself.

---

# Running the scraper

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

The result will be created:

```
output/series.csv
```