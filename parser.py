import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from config import SPLASH_URL

PARSED_PAGES = []


class Parser(object):

    _message_producer = None

    def __init__(self, message_producer, google_sheets):
        self._message_producer = message_producer
        self._google_sheets = google_sheets

    def parse(self, url):
        print("New url to parse")
        self._parse_by_url(url)
        print('______________End______________')

    def _parse_by_url(self, url):

        if url in PARSED_PAGES:
            print("Already parsed")
            return

        domain = self._get_domain_name(url)
        response = self._load_url(url)
        self._queueing_links_from_html(response.text, domain)
        self._google_sheets.insert([url, 1])
        PARSED_PAGES.append(url)

    def _load_url(self, url):
        print("URL loading ...")
        return requests.get(SPLASH_URL.format(url))

    def _queueing_links_from_html(self, html, domain):
        links = self._extract_links_from_html(html, domain)
        print("Extracted all links. Sending to queue.")
        self._send_links_to_queue(links)
        print("Sent")

    def _extract_links_from_html(self, html, domain):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            link_href = link.get('href')
            if link_href is not None:
                yield self._normalize_url(link_href, domain)

    def _send_links_to_queue(self, urls):
        for url in urls:
            if url not in PARSED_PAGES and url is not None:
                self._message_producer.send(url)

    def _normalize_url(self, url, domain):
        url = domain + url if url[0] == '/' else url
        return self._get_only_domain_and_path(url)

    def _get_domain_name(self, url):
        return urlparse(url).netloc

    def _get_only_domain_and_path(self, url):
        parsed = urlparse(url)
        return parsed.netloc + parsed.path
