from queue import Queue

import config
from document import Page


class ParsingQueue(object):

    def __init__(self):
        self.__queue = Queue()
        self.prepopulate()

    def put(self, url):
        if Page.objects.already_parsed(url=url):
            print(url, 'is already parsed. Cancel appending to queue')
            return

        if self.url_contains_blacklist(url):
            print('Blacklisted url')
            return

        self.__queue.put(url)

    def get(self):
        return self.__queue.get()

    def task_done(self):
        return self.__queue.task_done()

    def join(self):
        return self.__queue.join()

    def prepopulate(self):
        non_parsed = Page.objects.get_non_parsed()
        for page in non_parsed:
            self.put(page.url)

        print("Non parsed at start:", non_parsed.count())
        if non_parsed.count() == 0:
            self.populate_with_searches()

    def populate_with_searches(self):
        print("Populating from search:")
        for keyword in config.START_KEYWORDS:
            page = Page(url="https://www.google.com.ua/search?q={}+articles".format(keyword))
            page.save()
            self.put(page.url)

    @staticmethod
    def url_contains_blacklist(url):
        for domain in config.BLACKLIST_DOMAINS:
            if domain in url:
                print(domain, url)
                return True
        return False
