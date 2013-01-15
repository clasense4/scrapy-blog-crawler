# Scrapy Blog Crawler


This Crawler is for crawl some [Blog URL](http://tmcblog.com) like that,
and return some url that found on that url, then insert it into mysql.

## How to Use :
1. Clone this repository

        git clone https://github.com/clasense4/scrapy-blog-crawler.git

2. Edit `blog_crawler/settings.py` change your scrapy, redis and MySQL setting
3. Edit DEPTH_LIMIT if You want deeper crawling
4. Edit kaskus/spiders/new_kaskus_spider.py, change list of thread in this line:

        start_urls = ['http://tmcblog.com']

5. Insert this query :
        
        CREATE TABLE `scrapy_blog` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `url_from` varchar(255) NOT NULL,
          `url_found` varchar(255) NOT NULL,
          `url_referer` tinytext NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=MyISAM DEFAULT CHARSET=latin1


	CREATE TABLE `scrapy_blog_master` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `url_master` varchar(255) NOT NULL,
	  PRIMARY KEY (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='latin1_swedish_ci'

6. Make sure to start your redis server

	$> src/redis-server

7. And start your crawler with this command

        scrapy crawl blog_spider

8. At 20 December 2012, that script give me `2070` rows, with `DEPTH_LIMIT = 1`
9. At 8 January 2013, this script give me `749` Unique urls. And save in redis server using `sadd` command

## Notice
The script is still sucks, not follow scrapy standards, use at your own risks.

If You can improve this with pipelines, I'm really appreciated that.

mail me at clasense4[at]gmail[dot]com

[@clasense4](http://twitter.com/clasense4)
