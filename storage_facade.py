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
        validate_err = self.validate_url(url)
        if validate_err is not None:
            return validate_err

        self.__mongo.create_url(url)
        self.__queue.put(url)

    def url_parsed(self, url):
        self.__mongo.url_parsed(url)
        self.__queue.task_done()

    def get_url_from_queue(self):
        return self.__queue.get()

    def validate_url(self, url):
        if url in ['#', '', ' ']:
            return "URL is a hash or empty string. Abort"

        if self.__mongo.is_exists(url):
            return 'URL is already in queue. Abort'

        if self.url_with_blacklisted_domain(url):
            return 'Blacklisted url. Abort'
        return None

    @staticmethod
    def url_with_blacklisted_domain(url):
        for domain in config.BLACKLIST_DOMAINS:
            if domain in url:
                return True
        return False
