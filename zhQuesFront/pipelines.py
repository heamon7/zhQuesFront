# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import leancloud
from leancloud import Object
from leancloud import LeanCloudError
from leancloud import Query
from scrapy import log
from scrapy.exceptions import DropItem

from zhQuesFront import settings
import time
import bmemcached
import re

import redis

class FirstPipline(object):
    dbPrime = 997
    def __init__(self):
        leancloud.init(settings.APP_ID, master_key=settings.MASTER_KEY)
        #self.file = open('items.jl', 'wb')
        # self.client1 = bmemcached.Client(settings.CACHE_SERVER_1,settings.CACHE_USER_1,settings.CACHE_PASSWORD_1)
        # self.client2 = bmemcached.Client(settings.CACHE_SERVER_2,settings.CACHE_USER_2,settings.CACHE_PASSWORD_2)
        self.redis0 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_USER+':'+settings.REDIS_PASSWORD,db=0)
        self.redis1 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_USER+':'+settings.REDIS_PASSWORD,db=1)
    def process_item(self, item, spider):
        questionId = str(re.split('/question/',item['questionLinkHref'])[1])
        if self.redis1.exists(str(questionId)):
            pass
        else:
            tableIndex = int(item['questionTimestamp']) % self.dbPrime
            if tableIndex < 10:
                tableIndexStr = '00' + str(tableIndex)
            elif tableIndex < 100:
                tableIndexStr = '0' + str(tableIndex)
            else:
                tableIndexStr = str(tableIndex)

            Question = Object.extend('Question' + tableIndexStr)
            question = Question()

            questionIndex = self.redis0.incr('totalCount',1)
            p0= self.redis0.pipeline()

            p0.hsetnx('questionIndex',str(questionIndex),  str(questionId))
            p0.hsetnx('questionIdIndex',str(questionId),str(questionIndex))
            p0.execute()

            question.set('questionId',str(questionId))
            question.set('tableIndexStr',tableIndexStr)
            question.set('answerCount',item['answerCount'])
            question.set('isTopQuestion',item['isTopQuestion'])
            question.set('subTopicName',item['subTopicName'])
            question.set('subTopicHref',item['subTopicHref'])
            question.set('questionTimestamp',item['questionTimestamp'])
            question.set('questionLinkHref',item['questionLinkHref'])
            question.set('questionName',item['questionName'])

            question.set('questionIndex',str(questionIndex))



            # questionInfoList =[]
            # questionInfoList.append(str(questionIndex))
            # questionInfoList.append(str(tableIndexStr))
            # questionInfoList.append(str(item['questionTimestamp']))
            # questionInfoList.append(str(re.split('/topic(\d*)',item['subTopicHref'])))

            try:
                subTopicId = re.split('/topic/(\d*)',item['subTopicHref'])[1]
            except:
                subTopicId =0

            p1 = self.redis1.pipeline()
            p1.incr('totalCount',1)

            p1.rpush(str(questionId),int(questionIndex),int(tableIndexStr),int(item['questionTimestamp']),int(subTopicId))
            p1.execute()


            try:
                question.save()

            except LeanCloudError,e:
                try:
                    question.save()
                except LeanCloudError,e:
                    print e

        DropItem()


