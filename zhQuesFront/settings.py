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

CONCURRENT_REQUESTS = 70
CONCURRENT_REQUESTS_PER_DOMAIN = 70

SPIDER_MODULES = ['zhQuesFront.spiders']
NEWSPIDER_MODULE = 'zhQuesFront.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhQuesFront (+http://www.yourdomain.com)'

CACHE_SERVER_1 = 'd69c4508ccc94dc4.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211'
CACHE_USER_1 = 'd69c4508ccc94dc4'
CACHE_PASSWORD_1 = 'Zhihucache1'

# APP_ID_S = 'l72xkuuseu9sue0hn5xc0hhugw2ehalom2douyc0m8euw9og'
# MASTER_KEY_S = 'znl8sbojk3ait7f4xjbmofsui540eqin4ilncmz5z0qvs8ko'

APP_ID = '8scc82ncveedyt6p8ilcz2auzoahzvpu2y800m5075f9flp9'
MASTER_KEY = '06vseo6z44ummz0fgv0u6no7vnzqr4fbob0y2mxz6cv47p92'

ITEM_PIPELINES = {
    'zhQuesFront.pipelines.FirstPipline': 300,
   # 'zhihut.pipelines.SecondPipline': 800,
}
SPIDER_MIDDDLEWARES = {
    'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware':300,
}

DUPEFILTER_CLASS = 'zhQuesFront.custom_filters.SeenURLFilter'
