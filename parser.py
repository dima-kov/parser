import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from config import SPLASH_URL
from storage_facade import StorageFacade


class Parser(object):

    loop = None

    def __init__(self, storage_facade: StorageFacade):
        self.storage_facade = storage_facade

    async def parse(self, url):
        print("New url to parse")
        await self._parse_by_url(url)
        print('______________End______________')

    async def _parse_by_url(self, url):
        response = await self._load_url(url)
        self._queueing_links_from_html(url, response.text)
        self.storage_facade.url_parsed(url)

    async def _load_url(self, url):
        print("URL loading... Suspending...")
        return await self.loop.run_in_executor(None, requests.get, SPLASH_URL.format(url))

    def set_loop(self, loop):
        self.loop = loop

    def _queueing_links_from_html(self, url, html):
        links = self._extract_links_from_html(html, self._get_domain(url))
        print("Extracted all links. Sending to queue from URL {} .".format(url))
        self._send_links_to_queue(links)

    def _extract_links_from_html(self, html, domain):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            yield self._normalize_url(link.get('href', ''), domain)

    def _send_links_to_queue(self, urls):
        for url in urls:
            self.storage_facade.new_url(url)

    def _normalize_url(self, url, domain):
        """
            Appends domain if link without it.
        """
        return self._append_domain(url, domain)

    @staticmethod
    def _append_domain(url, domain):
        if url.startswith('//'):
            print("Url starts with double slash: ", url, "new: ", url[2:])
            return url[2:]

        if url.startswith('/'):
            print("Url starts with slash: ", url, "new: ", domain + url)
            return domain + url

        return url

    @staticmethod
    def _get_domain(url):
        print("domain: ", urlparse(url).netloc)
        return urlparse(url).netloc
