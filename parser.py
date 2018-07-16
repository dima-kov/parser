import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from config import SPLASH_URL
from document import Page


class Parser(object):

    def __init__(self, queue):
        self._queue = queue

    def parse(self, url):
        print("New url to parse")
        self._parse_by_url(url)
        print('______________End______________')

    def _parse_by_url(self, url):
        response = self._load_url(url)
        self._queueing_links_from_html(url, response.text)
        page_document = Page.objects.get_or_create(url=url)
        page_document.parsed_now()
        page_document.save()

    @staticmethod
    def _load_url(url):
        print("URL loading ...")
        return requests.get(SPLASH_URL.format(url))

    def _queueing_links_from_html(self, url, html):
        links = self._extract_links_from_html(html, self._get_domain(url))
        print("Extracted all links. Sending to queue.")
        self._send_links_to_queue(links)
        print("Sent")

    def _extract_links_from_html(self, html, domain):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            link_href = link.get('href')
            if link_href is not None and link_href not in ['#', '', ' ']:
                yield self._normalize_url(link_href, domain)

    def _send_links_to_queue(self, urls):
        for url in urls:
            self._queue.put(url)
            Page.objects.get_or_create(url=url)

    def _normalize_url(self, url, domain):
        if url[0] == '/':
            url = domain + url

        if url[0:2] == '//':
            url = domain + url[1:]
        return self._remove_hash(url)

    @staticmethod
    def _get_domain(url):
        return urlparse(url).netloc

    @staticmethod
    def _remove_hash(url):
        parsed = urlparse(url)
        return '{}://{}{}?{}'.format(parsed.scheme, parsed.netloc, parsed.path, parsed.query)
