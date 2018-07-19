import datetime

from mongoengine import QuerySet
from mongoengine import document
from mongoengine import fields


class PageQuerySet(QuerySet):

    def create(self, **kwargs):
        page = Page(**kwargs)
        page.save()
        return page

    def exists(self, **kwargs):
        return self.filter(**kwargs) .count() > 0

    def get_non_parsed(self):
        return self.filter(parsed=None)

    def get_parsed(self):
        return self.filter(parsed__ne=None)

    def get_or_create(self, url):
        pages = self.filter(url=url)
        if pages.count() == 0:
            page = Page(url=url)
            page.save()
            return page
        return pages.first()


class Page(document.Document):
    url = fields.StringField(required=True, max_length=6000, unique=True)
    parsed = fields.DateTimeField(required=False)
    created = fields.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'queryset_class': PageQuerySet}

    def parsed_now(self):
        self.parsed = datetime.datetime.utcnow()
