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

CACHE_SERVER_1 = 'd6fca732c8564f92.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211'
CACHE_USER_1 = 'd6fca732c8564f92'
CACHE_PASSWORD_1 = 'Zhihu7775'

CACHE_SERVER_2 = '83dda4c61e634a8f.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211'
CACHE_USER_2 = '83dda4c61e634a8f'
CACHE_PASSWORD_2 = 'Zhihu7776'


# APP_ID_S = 'l72xkuuseu9sue0hn5xc0hhugw2ehalom2douyc0m8euw9og'
# MASTER_KEY_S = 'znl8sbojk3ait7f4xjbmofsui540eqin4ilncmz5z0qvs8ko'

APP_ID = '041iof83iupmavqzsx3h6puivruvbhgbhhs8oenbfeo90e16'
MASTER_KEY = 'mfr0kdf9iz20ackcpmodjwvzyty73fcwcpfmqd19x8kxy915'

ITEM_PIPELINES = {
    'zhQuesFront.pipelines.FirstPipline': 300,
   # 'zhihut.pipelines.SecondPipline': 800,
}
SPIDER_MIDDDLEWARES = {
    'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware':300,
}

DUPEFILTER_CLASS = 'zhQuesFront.custom_filters.SeenURLFilter'
