import asyncio
from bs4 import BeautifulSoup
import aiohttp
import re

wikipedia_link_format = r"/wiki/[A-Za-z0-9_]+"
target_wikipedia_link = "https://en.wikipedia.org/wiki/Philosophy"

todo = asyncio.Queue()
seen_urls = set()
total_crawls = 0

async def add_links_to_crawl(soup: BeautifulSoup) -> None:
    website_links = soup.find_all('a')
    for link in website_links:
        href = link.get('href')
        if href and re.search(wikipedia_link_format, href):
            url = f"https://en.wikipedia.org{href}"
            if url not in seen_urls:
                await todo.put(url)
                seen_urls.add(url)


async def crawl(url: str) -> None:
    global total_crawls
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    page = await response.text()
                    soup = BeautifulSoup(page, 'html.parser')
                    if url == target_wikipedia_link:
                        print("Found philosophy!")
                        return

                    seen_urls.add(url)
                    await add_links_to_crawl(soup)
                    total_crawls += 1
                    print(f"Crawling: {url}")
                else:
                    print(f"Failed to crawl {url} (Status: {response.status})")
    except Exception as e:
        print(f"Error crawling {url}: {e}")


async def main():
    start_url = "https://en.wikipedia.org/wiki/Old_School_RuneScape"
    await todo.put(start_url)
    seen_urls.add(start_url)

    while True:
        if not todo.empty():
            next_url = await todo.get()
            await crawl(next_url)
        else:
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
