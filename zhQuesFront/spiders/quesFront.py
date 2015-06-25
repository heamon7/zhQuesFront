# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
# from scrapy.conf import settings

import logging

import redis
import requests

from zhQuesFront.items import zhQuesItem
from zhQuesFront import settings



class QuesfrontSpider(scrapy.Spider):
    name = "quesFront"
    allowed_domains = ["zhihu.com"]
    start_urls = ["http://www.zhihu.com/topic/19776749/questions"]
    handle_httpstatus_list = [429,504]

    def __init__(self,spider_type='Master',spider_number=0,partition=1,**kwargs):

        self.spider_type = str(spider_type)
        self.spider_number = int(spider_number)
        self.partition = int(partition)

    def parse(self, response):

        totalLength = int(response.xpath('//div[@class="border-pager"]//span[last()-1]/a/text()').extract()[0])
        self.requestPageList = range(1,totalLength+1)
        if self.spider_type=='Master':
            logging.warning('Master spider_type is '+self.spider_type)
            if self.partition!=1:
                logging.warning('Master non 1 partition is '+str(self.partition))
                self.requestPageList = self.requestPageList[self.spider_number*totalLength/self.partition:(self.spider_number+1)*totalLength/self.partition]

                for index in range(1,self.partition):
                    payload ={
                        'project':settings.BOT_NAME
                        ,'spider':self.name
                        ,'spider_type':'Slave'
                        ,'spider_number':index
                        ,'partition':self.partition
                        ,'setting':'JOBDIR=/tmp/scrapy/'+self.name+str(index)
                    }
                    logging.warning('Begin to request'+str(index))
                    response = requests.post('http://'+settings.SCRAPYD_HOST_LIST[index]+':'+settings.SCRAPYD_PORT+'/schedule.json',data=payload)
                    logging.warning('Response: '+str(index)+' '+str(response))
            else:
                logging.warning('Master  partition is '+str(self.partition))

        elif self.spider_type =='Slave':
            logging.warning('Slave spider_type is '+self.spider_type)
            logging.warning('Slave number is '+str(self.spider_number) + ' partition is '+str(self.partition))
            if (self.partition-self.spider_number)!=1:
                self.requestPageList = self.requestPageList[self.spider_number*totalLength/self.partition:(self.spider_number+1)*totalLength/self.partition]

            else:
                self.requestPageList = self.requestPageList[self.spider_number*totalLength/self.partition:]

        else:
            logging.warning('spider_type is:'+str(self.spider_type)+'with type of '+str(type(self.spider_type)))

        logging.warning('start_requests ing ......')
        logging.warning('totalCount to request is :'+str(len(self.requestPageList)))

        requestUrls =[]
        startUrl = self.start_urls[0]
        for index in self.requestPageList:
            page = startUrl + "?page=" + str(index)
            requestUrls.append(page)

        for reqUrl in requestUrls:
            yield  scrapy.Request(reqUrl,self.parsePage)


    def parsePage(self,response):
        if response.status != 200:
            yield Request(response.url,callback=self.parsePage)
        else:
            item = zhQuesItem()
            for sel in response.xpath('//div[@id="zh-topic-questions-list"]//div[@itemprop="question"]'):
                item['answerCount'] = int(sel.xpath('meta[@itemprop="answerCount"]/@content').extract()[0])
                item['isTopQuestion'] = sel.xpath('meta[@itemprop="isTopQuestion"]/@content').extract()[0]
                item['questionTimestamp'] = sel.xpath('h2[@class="question-item-title"]/span[@class="time"]/@data-timestamp').extract()[0]
                item['questionId'] = sel.xpath('h2[@class="question-item-title"]/a[@class="question_link"]/@href').re(r'/question/(\d*)')[0]

                try:
                    item['questionName'] = sel.xpath('h2[@class="question-item-title"]/a[@class="question_link"]/text()').extract()[0]
                except IndexError,e:
                    item['questionName'] = ''
                try:
                    item['subTopicName'] = sel.xpath('div[@class="subtopic"]/a/text()').extract()[0]
                    item['subTopicId'] = sel.xpath('div[@class="subtopic"]/a/@href').re(r'/topic/(\d*)')[0]

                except IndexError,e:
                    item['subTopicName'] = ''
                    item['subTopicId'] = 0

                yield item

    def closed(self,reason):
        self.redis15 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD,db=15)
        #这样的顺序是为了防止两个几乎同时结束
        p15=self.redis15.pipeline()
        p15.lpush(str(self.name),self.spider_number)
        p15.llen(str(self.name))
        finishedCount= p15.execute()[1]

        if int(self.partition)==int(finishedCount):
            payload=settings.NEXT_SCHEDULE_PAYLOAD
            logging.warning('Begin to request next schedule')
            response = requests.post('http://'+settings.NEXT_SCHEDULE_SCRAPYD_HOST+':'+settings.NEXT_SCHEDULE_SCRAPYD_PORT+'/schedule.json',data=payload)
            logging.warning('Response: '+' '+str(response))
        logging.warning('finished close.....')





 # self.stats = stats
        #print "Initianizing ....."
        # self.redis0 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_USER+':'+settings.REDIS_PASSWORD,db=0)




    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(crawler.stats)



                        #
                # for index ,questionId in enumerate(self.questionIdList):
                #     p2.lindex(str(questionId),6)
                #     if index%self.pipelineLimit ==0:
                #         self.questionFollowerCountList.extend(p2.execute())
                #     elif questionIdListLength-index==1:
                #         self.questionFollowerCountList.extend(p2.execute())
                #     # p2 = self.redis2.pipeline()
