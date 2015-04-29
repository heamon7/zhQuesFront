# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings

from scrapy import log


from zhQuesFront.items import zhQuesItem


rootTopicPageNum = 0

class QuesfrontSpider(scrapy.Spider):
    name = "quesFront"
    allowed_domains = ["zhihu.com"]
    start_urls = ["http://www.zhihu.com/topic/19776749/questions"]



    def parse(self, response):

        rootTopicPageNum = int(response.xpath('//div[@class="border-pager"]//span[last()-1]/a/text()').extract()[0])

        requestUrls =[]
        startUrl = self.start_urls[0]
        for index in range(0,5):
            page = startUrl + "?page=" + str(index)
            requestUrls.append(page)

        for reqUrl in requestUrls:
            yield  scrapy.Request(reqUrl,self.parsePage)


    def parsePage(self,response):
        item = zhQuesItem()
        for sel in response.xpath('//div[@id="zh-topic-questions-list"]//div[@itemprop="question"]'):
            item['answerCount'] = int(sel.xpath('meta[@itemprop="answerCount"]/@content').extract()[0])
            item['isTopQuestion'] = sel.xpath('meta[@itemprop="isTopQuestion"]/@content').extract()[0]
            item['questionTimestamp'] = sel.xpath('h2[@class="question-item-title"]/span[@class="time"]/@data-timestamp').extract()[0]
            item['questionLinkHref'] = sel.xpath('h2[@class="question-item-title"]/a[@class="question_link"]/@href').extract()[0]
            item['questionName'] = sel.xpath('h2[@class="question-item-title"]/a[@class="question_link"]/text()').extract()[0]
            try:
                item['subTopicName'] = sel.xpath('div[@class="subtopic"]/a/text()').extract()[0]
                item['subTopicHref'] = sel.xpath('div[@class="subtopic"]/a/@href').extract()[0]

            except IndexError,e:
                item['subTopicName'] = ''
                item['subTopicHref'] = ''
                log.msg("No subTopic question: "+item['questionLinkHref'],level=Warning)
                print e
            # item['link'] = sel.xpath('')
            # item['desc'] = sel.xpath('')
            # item['link'] = sel.xpath('')
            # item['link'] = sel.xpath('')

            yield item






