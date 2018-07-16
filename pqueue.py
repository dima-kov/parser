from queue import Queue

import config
from document import Page


def prepopulate_queue():

    queue = Queue()

    non_parsed = Page.objects.get_non_parsed()
    for page in non_parsed:
        queue.put(page.url)

    print("Non parsed at start:", non_parsed.count())
    if non_parsed.count() == 0:
        print("Non parsed  is zero. Populating from search:")
        populate_with_searches(queue)

    return queue


def populate_with_searches(queue):
    for keyword in config.START_KEYWORDS:
        page = Page(url="https://www.google.com.ua/search?q={}+articles".format(keyword))
        page.save()
        queue.put(page.url)
