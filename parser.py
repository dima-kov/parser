import requests

from bs4 import BeautifulSoup

from config import SPLASH_URL

PARSED_PAGES = []


class Parser(object):

    _message_producer = None

    def __init__(self, message_producer):
        self._message_producer = message_producer

    def parse(self, url):
        print("New url to parse")
        self._parse_url(url)
        print('______________End______________')

    def _parse_url(self, url):
        if url in PARSED_PAGES:
            print("Already parsed")
            return

        response = self._load_url(url)
        self._queueing_links_from_html(response.text)
        PARSED_PAGES.append(url)

    def _load_url(self, url):
        print("URL loading ...")
        return requests.get(SPLASH_URL.format(url))

    def _queueing_links_from_html(self, html):
        links = self._extract_links_from_html(html)
        print("Extracted all links. Sending to queue.")
        self._send_links_to_queue(links)
        print("Sent")

    def _extract_links_from_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return [link.get('href') for link in soup.find_all('a')]

    def _send_links_to_queue(self, urls):
        for url in urls:
            if url not in PARSED_PAGES and url is not None:
                self._message_producer.send(url)
