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


class FirstPipline(object):
    dbPrime = 97
    def __init__(self):
        leancloud.init('8scc82ncveedyt6p8ilcz2auzoahzvpu2y800m5075f9flp9', master_key='06vseo6z44ummz0fgv0u6no7vnzqr4fbob0y2mxz6cv47p92')
        #self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        tableIndex = int(item['questionTimestamp']) % self.dbPrime
        if tableIndex < 10:
            tableIndexStr = '0' + str(tableIndex)
        else:
            tableIndexStr = str(tableIndex)
        Question = Object.extend('Question' + tableIndexStr)
        question = Question()
#        query = Query(Question)
        try:
 #           query.equal_to('questionLinkHref',item['questionLinkHref'])

  #          if not query.find():
	    if 1:
                question.set('tableIndex',tableIndex)
                question.set('answerCount',item['answerCount'])
                question.set('isTopQuestion',item['isTopQuestion'])
                question.set('subTopicName',item['subTopicName'])
                question.set('subTopicHref',item['subTopicHref'])
                question.set('questionTimestamp',item['questionTimestamp'])
                question.set('questionLinkHref',item['questionLinkHref'])
                question.set('questionName',item['questionName'])
                question.save()
                #print "Question saved: %s" %item['questionLinkHref']
            else:
#               # print "Question existed: %s" %item['questionLinkHref']
		pass
        except LeanCloudError,e:
            print e
        finally:
            DropItem()


