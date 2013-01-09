# Scrapy settings for blog_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import sys
import MySQLdb

BOT_NAME = 'blog_crawler'
BOT_VERSION = '1.0'

# SCRAPY SETTING
SPIDER_MODULES = ['blog_crawler.spiders']
NEWSPIDER_MODULE = 'blog_crawler.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
DEPTH_LIMIT = 1

ITEM_PIPELINES = [
    'blog_crawler.pipelines.SQLStorePipeline',
]

# SQL DATABASE SETTING
SQL_DB = 'scrapy'
SQL_TABLE = 'scrapy_blog'
SQL_TABLE_MASTER = 'scrapy_blog_master'
SQL_HOST = 'localhost'
SQL_USER = 'root'
SQL_PASSWD = '54321'

# REDIS SERVER SETTING
REDIS_SERVER = 'localhost'
REDIS_PORT = 6380

# connect to the MySQL server
try:
    CONN = MySQLdb.connect(host=SQL_HOST,
                         user=SQL_USER,
                         passwd=SQL_PASSWD,
                         db=SQL_DB)
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
