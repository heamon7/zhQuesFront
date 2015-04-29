# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class zhQuesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    answerCount = scrapy.Field()
    isTopQuestion = scrapy.Field()
    subTopicName = scrapy.Field()
    subTopicHref = scrapy.Field()
    questionTimestamp = scrapy.Field()
    questionLinkHref = scrapy.Field()
    questionName = scrapy.Field()

    # link = scrapy.Field()
    # desc = scrapy.Field()

    # 现在只想得到所有的问题，所以不考虑其他的信息，对于子话题等信息，用另外一个crawler爬取
    # rootTopicPageNum = scrapy.Field()  
    # rootTopicFollowerNum = scrapy.Field()
    # childTopicIdList = scrapy.Field()



