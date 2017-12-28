# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from .sql import Sql
from twisted.internet.threads import deferToThread
from jobs.items import JobsItem
from scrapy.exceptions import DropItem

class JobsPipeline(object):

    def process_item(self, item, spider):
        spider.logger.info("in pipeline")
        #deferToThread(self._process_item, item, spider)
        if isinstance(item, JobsItem):
            job_id = item['job_id']
            ret = Sql.select_id(job_id)
            if ret[0] == 1:
#                spider.logger.info('dup item :' + job_id)
#                spider.LAW_LOG.append('dup item :' + job_id)
                raise DropItem("dup item in %s" % item)
            else:
                name = item['name']
                job_id = item['job_id']
                company = item['company']
                vacant = item['vacant'] 
                detail = item['detail'] 
                salary = item['salary'] 
                area = item['area'] 
                date_posted = item['date_posted']
#(cls, name,job_id, company, detail, industry,salary,area,vacant,date_posted):
                (Sql.insert_jobs(spider,name, job_id, company, detail,'',salary,area,vacant,date_posted))
                spider.logger.info('save to db :' + job_id)
#                spider.LAW_LOG.append('save to db :' + job_id)