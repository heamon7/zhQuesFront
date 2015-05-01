# -*- coding: utf-8 -*-

# Scrapy settings for zhQuesFront project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'zhQuesFront'


CONCURRENT_REQUESTS = 50
CONCURRENT_REQUESTS_PER_DOMAIN = 50

SPIDER_MODULES = ['zhQuesFront.spiders']
NEWSPIDER_MODULE = 'zhQuesFront.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhQuesFront (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'zhQuesFront.pipelines.FirstPipline': 300,
   # 'zhihut.pipelines.SecondPipline': 800,
}
SPIDER_MIDDDLEWARES = {
    'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware':300,
}

DUPEFILTER_CLASS = 'zhQuesFront.custom_filters.SeenURLFilter'
