# -*- coding: utf-8 -*-

# Scrapy settings for zhQuesFront project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'zhQuesFront'
LOG_LEVEL = 'INFO'
DOWNLOAD_TIMEOUT = 700

SPIDER_MODULES = ['zhQuesFront.spiders']
NEWSPIDER_MODULE = 'zhQuesFront.spiders'

ITEM_PIPELINES = {
    'zhQuesFront.pipelines.FirstPipline': 300,
   # 'zhihut.pipelines.SecondPipline': 800,
}

SPIDER_MIDDDLEWARES = {
    'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware':300,
}

DUPEFILTER_CLASS = 'zhQuesFront.custom_filters.SeenURLFilter'

CONCURRENT_REQUESTS = 70
CONCURRENT_REQUESTS_PER_DOMAIN = 70

UPDATE_PERIOD = '864000' #最快10天更新一次
EXTENSIONS = {
    'scrapy.contrib.feedexport.FeedExporter': None,
    'scrapy.extensions.feedexport.FeedExporter': None
}

