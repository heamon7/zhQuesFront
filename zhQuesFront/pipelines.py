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

class FirstPipline(object):
    dbPrime = 97
    def __init__(self):
        leancloud.init(settings.APP_ID, master_key=settings.MASTER_KEY)
        #self.file = open('items.jl', 'wb')
        self.client1 = bmemcached.Client(settings.CACHE_SERVER_1,settings.CACHE_USER_1,settings.CACHE_PASSWORD_1)
        self.client2 = bmemcached.Client(settings.CACHE_SERVER_2,settings.CACHE_USER_2,settings.CACHE_PASSWORD_2)
    def process_item(self, item, spider):
        questionId = str(re.split('/question/',item['questionLinkHref'])[1])
        if self.client1.get(str(questionId)):
            pass
        else:
            tableIndex = int(item['questionTimestamp']) % self.dbPrime
            if tableIndex < 10:
                tableIndexStr = '0' + str(tableIndex)
            else:
                tableIndexStr = str(tableIndex)

            Question = Object.extend('Question' + tableIndexStr)
            question = Question()

            self.client1.incr('totalCount',1)
            questionIndex = self.client2.incr('totalCount',1)
            questionInfoList =[]
            questionInfoList.append(int(questionIndex))
            questionInfoList.append(int(tableIndexStr))
            # questionInfoList.append(int(item['questionTimestamp']))

            self.client1.set(str(questionId),questionInfoList)
            self.client2.set(str(questionIndex),int(questionId))

            question.set('questionId',str(questionId))
            question.set('tableIndex',tableIndex)
            question.set('answerCount',item['answerCount'])
            question.set('isTopQuestion',item['isTopQuestion'])
            question.set('subTopicName',item['subTopicName'])
            question.set('subTopicHref',item['subTopicHref'])
            question.set('questionTimestamp',item['questionTimestamp'])
            question.set('questionLinkHref',item['questionLinkHref'])
            question.set('questionName',item['questionName'])

            question.set('questionIndex',str(questionIndex))


            try:
                question.save()

            except LeanCloudError,e:
                try:
                    question.save()
                except LeanCloudError,e:
                    print e

        DropItem()


