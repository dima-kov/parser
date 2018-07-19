import config
from mongo import PageMongoStorage
from pqueue import ParsingQueue


class StorageFacade(object):
    """
        Facade class to encapsulate behaviour of parser and queue handler
        with queue and mongo storage
    """
    __mongo = None
    __queue = None

    def __init__(self, mongo: PageMongoStorage, queue: ParsingQueue):
        self.__mongo = mongo
        self.__queue = queue

    def new_url(self, url):
        try:
            self.validate_url(url)
        except ValueError as e:
            print("URL error: ", url, e)
            return
        print("URL is ok: ", url)
        self.__mongo.create_url(url)
        self.__queue.put(url)

    def url_parsed(self, url):
        self.__mongo.url_parsed(url)
        self.__queue.task_done()

    def queue_empty(self):
        return self.__queue.empty()

    def get_url_from_queue(self):
        return self.__queue.get()

    def validate_url(self, url):
        if url in ['#', '', ' ']:
            raise ValueError("URL is a hash or empty string. Abort")

        if url.startswith('#'):
            raise ValueError("URL is a anchor. Abort")

        if url.startswith('javascript'):
            raise ValueError("URL is a javascript function. Abort")

        if url.startswith('mailto'):
            raise ValueError("URL is a mailto link. Abort")

        if url.startswith('tel'):
            raise ValueError("URL is a telephone link. Abort")

        if len(url) > 2000:
            raise ValueError("URL is too long. Abort")

        if self.url_with_blacklisted_domain(url):
            raise ValueError("Blacklisted url. Abort")

        if self.__mongo.is_exists(url):
            raise ValueError("URL is already in queue. Abort")

    @staticmethod
    def url_with_blacklisted_domain(url):
        for domain in config.BLACKLIST_DOMAINS:
            if domain in url:
                return True
        return False
