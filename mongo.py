from document import Page


class PageMongoStorage(object):

    @staticmethod
    def create_url(url):
        Page.objects.create(url=url)

    @staticmethod
    def url_parsed(url):
        page = Page.objects.get(url=url)
        page.parsed_now()
        page.save()

    @staticmethod
    def is_exists(url):
        return Page.objects.exists(url=url)

    @staticmethod
    def is_already_parsed(url):
        return Page.objects.already_parsed(url=url)
