from queue import Queue

import config
from document import Page


class ParsingQueue(object):

    def __init__(self):
        self.__queue = Queue()
        self.prepopulate()

    def put(self, url):
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
            page = Page()
            page.url = "https://www.google.com.ua/search?q={}+articles".format(keyword)
            page.save()
            self.put(page.url)

