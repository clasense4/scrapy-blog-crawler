# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

# Cannot use this to create the table, must have table already created

from twisted.enterprise import adbapi
# import datetime
import MySQLdb.cursors

# class BlogCrawlerPipeline(object):
#     def process_item(self, item, spider):
#         return item


class SQLStorePipeline(object):

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='scrapy',
                user='root', passwd='54321', cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        # query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist.
        # all this block run on it's own thread
        # tx.execute("select * from websites where link = %s", (item['link'][0], ))
        # result = tx.fetchone()
        # if result:
        #     log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
        # else:
        #     tx.execute(\
        #         "insert into websites (link, created) "
        #         "values (%s, %s)",
        #         (item['link'][0],
        #          datetime.datetime.now())
        #     )
        print("Item stored in db: %s" % item)

    # def handle_error(self, e):
    #     log.err(e)

# Snippet imported from snippets.scrapy.org (which no longer works)
# author: redtricycle
# date  : Nov 21, 2011
