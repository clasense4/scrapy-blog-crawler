from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from blog_crawler.items import *
from scrapy.http import Request
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import pprint
import re
import urlparse
from blog_crawler.settings import *
import redis
import urlparse

'''
Local VARIABLE
'''
cursor = CONN.cursor()
pp = pprint.PrettyPrinter(indent=4)
r = redis.Redis("localhost")


def exclude_self(url, response_url, mode):
    # mode 1 = Outer url
    if mode == 1:
        if response_url not in url:
            return url
    # mode 2 = Inner url
    elif mode == 2:
        if response_url in url:
            return url


def clean(url):
    # regex to check valid url
    regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    try:
        u = regex.match(url).group()
        # print "%s valid url" % u
        return u
    except:
        # return "not valid url"
        pass


def clean_www(url):
    if 'www.' in url:
        return url.replace('www.', '')
    else:
        return url


def get_base_url(url):
    if url != "":
        u = urlparse.urlparse(url)
        """
        >>> urlparse.urlparse('http://tmcblog.com')
        >>> ParseResult(scheme='http', netloc='tmcblog.com', path='', params='', query='', fragment='')
        """
        return "%s://%s" % (u.scheme, u.netloc)
    else:
        return ""


def insert_table(url_from, url_found, url_referer):
#     sql = "INSERT INTO %s(url_from, url_found, url_referer) \
# values('%s', '%s', '%s')" % (SQL_TABLE, MySQLdb.escape_string(url_from), \
    # MySQLdb.escape_string(url_found), MySQLdb.escape_string(url_referer))
    sql = "INSERT INTO %s(url_from, url_found, url_referer) \
values('%s', '%s', '%s')" % (SQL_TABLE, url_from, \
    url_found, url_referer)
    # print sql
    if cursor.execute(sql):
        return True
    else:
        print "Something wrong"


def insert_redis(command, key1, key2):
    # r.sadd(key1, key2)
    if command == 'sadd':
        if r.sadd(key1, key2):
            return True
    if command == 'set':
        if r.set(key1, key2):
            return True


class BlogSpider(CrawlSpider):
    name = 'blog_spider'
    # allowed_domains = ['detik.com']
    # start_urls = ['http://detik.com']
    start_urls = ['http://tmcblog.com']

    # rules = (
    #     # Rule(SgmlLinkExtractor(allow=('(?:http|ftp)s?://',), attrs=('href')), follow=True, callback='parse'),
    #     Rule(SgmlLinkExtractor(), callback='parse'),
    # )

    def parse(self, response):
        # VARIABLE
        self.log('Main page %s' % response.url)
        # base_url = response.url.split('/')[2]
        # base_url = clean_www(response.url)
        base_url = get_base_url(response.url)
        hxs = HtmlXPathSelector(response)

        self.log('Base URL %s' % base_url)
        # HXS select URL onlye
        link = hxs.select('//a/@href').extract()

        '''
        Extract Outer Link
        '''
        outer_link = [exclude_self(l, base_url, 1) for l in set(link)]
        # self.log('Outer URL')
        outer_link = filter(None, outer_link)
        outer_link = filter(clean, outer_link)
        # print "Count = %s" % len(outer_link)
        # print "Count = %s" % len(set(outer_link))
        # pp.pprint((outer_link))
        # print outer_link

        # '''
        # Extract Inner Link
        # '''
        # inner_link = [exclude_self(l, base_url, 2) for l in set(link)]
        # self.log('Inner URL')
        # inner_link = filter(None, inner_link)
        # inner_link = filter(clean, inner_link)
        # # print "Count = %s" % len(inner_link)
        # # print "Count = %s" % len(set(inner_link))
        # pp.pprint((inner_link))

        '''
        Save Our Item
        '''
        blog = BlogCrawlerItem()
        blog['url_from'] = base_url
        blog['url_outer'] = outer_link
        try:
            temp = response.meta['redirect_urls']
            # looping & join multiple redirect url
            if not isinstance(temp, basestring):
                blog['url_refer'] = ','.join(i for i in temp)
                print blog['url_refer']
            else:
                blog['url_refer'] = temp
        except:
            blog['url_refer'] = ""
        # blog['url_inner'] = inner_link

        '''
        Save to MySQL, looping by outer_link
        '''
        for out in blog['url_outer']:
            if insert_redis('sadd', get_base_url(blog['url_from']), get_base_url(out)):
                insert_table(get_base_url(blog['url_from']), get_base_url(out), get_base_url(blog['url_refer']))
                # print "insert_redis"
            # insert_redis('sadd', blog['url_from'], out)

        '''
        Print Item
        '''
        # print blog
        for url in outer_link:
            yield Request(url, callback=self.parse)
