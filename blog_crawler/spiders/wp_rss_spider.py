from scrapy.spider import BaseSpider
from blog_crawler.settings import *
# from scrapy.selector import HtmlXPathSelector
# from scrapy.selector import XmlXPathSelector
# from scrapy.http import Request
import feedparser

cursor = CONN.cursor()


def add_feed(url):
    return url + "/feed/"


class RSSSpider(BaseSpider):
    name = "wp_rss_spider"
    # start_urls = [
    #     "http://news.google.com/"
    # ]

    # Select url from db
    # cursor.execute("")
    sql = "SELECT url_master FROM scrapy_blog_master WHERE class='WP' LIMIT 2"
    cursor.execute(sql)
    # start_urls = [add_feed(url) for url in cursor.fetchall()[0]]
    start_urls = [add_feed(row[0]) for row in cursor.fetchall()]

    def parse(self, response):
        # Just Print
        # print "RSS " + response.url
        p = feedparser.parse(response.body)
        for entries in p['entries']:
            print "RSS " + response.url
            if entries['content']:
                print "Ini CONTENT"
                print entries['content'][0]['value']
            if entries['summary']:
                print "Ini SUMMARY"
                print entries['summary']
