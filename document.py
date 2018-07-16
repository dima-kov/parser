import datetime

from mongoengine import connection, QuerySet
from mongoengine import document
from mongoengine import fields

from config import MONGO_DB_NAME
from config import MONGO_HOST
from config import MONGO_PORT


connection.connect(MONGO_DB_NAME, host=MONGO_HOST, port=MONGO_PORT)


class PageQuerySet(QuerySet):

    def create(self, **kwargs):
        page = Page(**kwargs)
        page.save()
        return page
    
    def get_non_parsed(self):
        return self.filter(parsed=None)
    
    def get_or_create(self, url):
        pages = self.filter(url=url)
        if pages.count() == 0:
            page = Page(url=url)
            page.save()
            return page
        return pages.first()


class Page(document.Document):
    url = fields.StringField(required=True, max_length=600, unique=True)
    created = fields.DateTimeField(default=datetime.datetime.utcnow)
    parsed = fields.DateTimeField(required=False)

    meta = {'queryset_class': PageQuerySet}

    def parsed_now(self):
        self.parsed = datetime.datetime.utcnow()
