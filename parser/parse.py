import requests
from config import SPLASH_URL

PARSED_PAGES = []


class Parser(object):

    _message_producer = None

    def __init__(self, message_producer):
        self._message_producer = message_producer

    def parse(self, url):
        print("Start parsing...")
        self._parse_url(url)

    def _parse_url(self, url):
        if url in PARSED_PAGES:
            print("Already parsed")
            return
        response = self._load_url(url)
        all_links = self._extract_links_from_html(response.text)
        self._send_links_to_queue(all_links)
        PARSED_PAGES.append(url)

    def _load_url(self, url):
        return requests.get(SPLASH_URL.format(url))

    def _extract_links_from_html(self, html):
        return []

    def _send_links_to_queue(self, urls):
        for url in urls:
            if url not in PARSED_PAGES:
                self._message_producer.send(url)
