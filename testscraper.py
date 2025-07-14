import asyncio
from bs4 import BeautifulSoup
import aiohttp
import re

wikipedia_link_format = r"/wiki/[A-Za-z0-9_]+"
target_wikipedia_link = "https://en.wikipedia.org/wiki/Philosophy"
start_url = "https://en.wikipedia.org/wiki/Dead_by_Daylight"

todo = asyncio.Queue()
seen_urls = set()
blacklisted_urls = ['https://en.wikipedia.org/wiki/Main_Page'] #Don't want to make it too easy
url_parents = {}
total_crawls = 0
num_crawlers = 25
found_target = asyncio.Event()

use_first_link_only = True

async def add_links_to_crawl(soup: BeautifulSoup, parent_url) -> None:
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        website_links = p.find_all('a')
        for link in website_links:
            href = link.get('href')
            if href and re.search(wikipedia_link_format, href):
                url = f"https://en.wikipedia.org{href}"
                if url not in seen_urls and url not in blacklisted_urls:
                    await todo.put(url)
                    seen_urls.add(url)
                    url_parents[url] = parent_url
                    if use_first_link_only:
                        return 
        if use_first_link_only:
            continue

async def crawler(session: aiohttp.ClientSession) -> None:
    while True:
        url = await todo.get()
        try:
            await crawl(url, session)
        finally:
            todo.task_done()
            
async def crawl(url: str, session: aiohttp.ClientSession) -> None:
    global total_crawls
    if found_target.is_set():
        return
    try:
        async with session.get(url) as response:
            if response.status == 200:
                page = await response.text()
                soup = BeautifulSoup(page, 'html.parser')
                if url == target_wikipedia_link:
                    print("Found philosophy!")
                    found_target.set()
                    print_path_to_target(url)
                    return

                if not found_target.is_set():
                    seen_urls.add(url)
                    await add_links_to_crawl(soup, url)
                    total_crawls += 1
                    print(f"Crawling: {url}")
            else:
                if not found_target.is_set():
                    print(f"Failed to crawl {url} (Status: {response.status})")
    except Exception as e:
        print(f"Error crawling {url}: {e}")

def print_path_to_target(target_url: str) -> None:
    path = []
    current = target_url
    while current:
        path.append(current)
        current = url_parents.get(current)
    path.reverse()
    print("The path to philosphy:")
    for step in path:
        print(step)
        
        
async def main():
    await todo.put(start_url)
    seen_urls.add(start_url)
    
    async with aiohttp.ClientSession() as session:
        workers = [asyncio.create_task(crawler(session)) for _ in range(num_crawlers)]
        await todo.join()
        for w in workers:
            w.cancel()
        

if __name__ == "__main__":
    asyncio.run(main())
