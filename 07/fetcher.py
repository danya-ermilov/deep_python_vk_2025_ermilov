import asyncio
import argparse
import re
from collections import Counter
from bs4 import BeautifulSoup
import aiohttp


class URLFetcher:
    def __init__(self, concurrency: int):
        self.concurrency = concurrency
        self.semaphore = asyncio.Semaphore(concurrency)

    async def fetch(self, session: aiohttp.ClientSession, url: str):
        async with self.semaphore:
            try:
                async with session.get(url, timeout=10) as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    text = soup.get_text()
                    top_words = self.get_top_words(text, top_n=5)
                    return url, response.status, top_words
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                return url, None, []

    def get_top_words(self, text: str, top_n=5):
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        counter = Counter(words)
        return counter.most_common(top_n)

    async def run(self, urls):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in urls]
            return await asyncio.gather(*tasks)


def load_urls(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def parse_args():
    parser = argparse.ArgumentParser(description="Async URL fetcher with word frequency analysis")
    parser.add_argument('concurrency', type=int, help="Number of concurrent requests")
    parser.add_argument('file', type=str, help="Path to file with URLs")
    return parser.parse_args()


async def main():
    args = parse_args()
    urls = load_urls(args.file)

    fetcher = URLFetcher(args.concurrency)
    await fetcher.run(urls)

if __name__ == "__main__":
    asyncio.run(main())
