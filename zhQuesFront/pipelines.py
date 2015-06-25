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
import re

import redis
import happybase
class FirstPipline(object):
    # dbPrime = 997
    def __init__(self):
        self.redis0 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD,db=0)
        self.redis1 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD,db=1)
        connection = happybase.Connection(settings.HBASE_HOST)
        self.questionTable = connection.table('question')

    def process_item(self, item, spider):

        #保证此次操作的原子性,其实如果是分布式的话，因为有分割，应该是不会冲突的，但是随着时间的增加还是有可能交叉
        #如果正在更新当前这个问题的data ：
        if  self.redis0.hsetnx('questionLock',str(item['questionId']),1):
            #使用try，是为了确保锁会被解除。
            try:
                currentTimestamp = int(time.time())

                result = self.redis1.lrange(str(item['questionId']),0,1)
                if result:
                    [recordTimestamp,questionIndex]=result
                else:
                    [recordTimestamp,questionIndex]=('','')

                p0= self.redis0.pipeline()
                p1 = self.redis1.pipeline()
                if not recordTimestamp:
                    questionIndex = self.redis0.incr('totalCount',1)

                    p0.hsetnx('questionIndex'
                              ,str(questionIndex)
                              ,str(item['questionId']))
                    p0.hsetnx('questionIdIndex'
                              ,str(item['questionId'])
                              ,str(questionIndex))
                    p0.execute()

                    p1.incr('totalCount',1)
                    p1.lpush(str(item['questionId'])
                                 ,str(item['questionTimestamp'])
                                 ,str(item['subTopicId'])
                                 ,str(questionIndex)
                                 ,str(recordTimestamp))
                    p1.execute()

                isTopQuestion = 1 if item['isTopQuestion'] == 'true' else 0
                # 为了防止第一次插入数据库失败，需要以后有更新操作，这里更新时间可以设置长一些
                if not recordTimestamp or (int(currentTimestamp)-int(recordTimestamp) > int(settings.UPDATE_PERIOD)):        # the latest record time in hbase
                    recordTimestamp = currentTimestamp
                    try:
                        self.questionTable.put(str(item['questionId']),{'basic:quesId':str(item['questionId']),
                                                           'basic:answerCount':str(item['answerCount']),
                                                           'basic:isTopQues':str(isTopQuestion),
                                                           'basic:subTopicName':item['subTopicName'].encode('utf-8'),
                                                           'basic:subTopicId':str(item['subTopicId']),
                                                           'basic:quesTimestamp':str(item['questionTimestamp']),
                                                           'basic:quesName':item['questionName'].encode('utf-8'),
                                                           'basic:quesIndex':str(questionIndex)})
                    except Exception,e:
                        log.msg('Error with put questionId into hbase: '+str(e)+' try again......',level=log.ERROR)
                        try:
                            self.questionTable.put(str(item['questionId']),{'basic:quesId':str(item['questionId']),
                                                       'basic:answerCount':str(item['answerCount']),
                                                       'basic:isTopQues':str(isTopQuestion),
                                                       'basic:subTopicName':item['subTopicName'].encode('utf-8'),
                                                       'basic:subTopicId':str(item['subTopicId']),
                                                       'basic:quesTimestamp':str(item['questionTimestamp']),
                                                       'basic:quesName':item['questionName'].encode('utf-8'),
                                                       'basic:quesIndex':str(questionIndex)})
                            log.msg(' tried again and successfully put data into hbase ......',level=log.ERROR)
                        except Exception,e:
                            log.msg('Error with put questionId into hbase: '+str(e)+'tried again and failed',level=log.ERROR)
                    #更新记录的时间戳
                    self.redis1.lset(str(item['questionId']),0,str(recordTimestamp))
            except Exception,e:
                log.msg('Error in try 0 with exception: '+str(e),level=log.ERROR)

            #解除锁
            self.redis0.hdel('questionLock',str(item['questionId']))
        DropItem()


            # question.set('questionId',str(questionId))
            # # question.set('tableIndexStr',tableIndexStr)
            # question.set('answerCount',item['answerCount'])
            # question.set('isTopQuestion',item['isTopQuestion'])
            # question.set('subTopicName',item['subTopicName'])
            # question.set('subTopicHref',item['subTopicHref'])
            # question.set('questionTimestamp',item['questionTimestamp'])
            # # question.set('questionLinkHref',item['questionLinkHref'])
            # question.set('questionName',item['questionName'])
            #
            # question.set('questionIndex',str(questionIndex))



            # questionInfoList =[]
            # questionInfoList.append(str(questionIndex))
            # questionInfoList.append(str(tableIndexStr))
            # questionInfoList.append(str(item['questionTimestamp']))
            # questionInfoList.append(str(re.split('/topic(\d*)',item['subTopicHref'])))



            #
            # try:
            #     question.save()
            #
            # except LeanCloudError,e:
            #     try:
            #         question.save()
            #     except LeanCloudError,e:
            #         print "The exception is %s" %str(e)



