# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class BlogCrawlerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    # pass
    url_from = Field()
    url_outer = Field()
    url_refer = Field()

    # def __str__(self):
    #     return "URL: name=%s" % (self.get('url_from'))
