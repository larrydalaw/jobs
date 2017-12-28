''' 
  class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    # score 

    #movie_id
    job_id = scrapy.Field()
    #category
    company=scrapy.Field()
    #director
    detail = scrapy.Field()
    #scriptwriter 
    industry = scrapy.Field()
    #movie_category 
    salary = scrapy.Field()
    area = scrapy.Field()
    #language 
    vacant = scrapy.Field()
    #date
    date_posted = scrapy.Field()
    #time = scrapy.Field()
    #byname = scrapy.Field()
    '''

import mysql.connector
from jobs import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cur = cnx.cursor(buffered=True)

class Sql:
    '''
    @classmethod
    def insert_jobs(cls, name, job_id, company):
        sql = 'INSERT INTO job (`name`, `job_id`, `company`) VALUES (%(name)s,  %(job_id)s, %(company)s)'
        value = {
            'name': name,
            'job_id': job_id,
            'company': company
        }
        cur.execute(sql, value)
        cnx.commit()
'''
    @classmethod
    def select_id(cls, job_id):
        sql = "SELECT EXISTS(SELECT 1 FROM job WHERE job_id=%(job_id)s)"
        value = {
            'job_id': job_id
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]

    @classmethod
    def insert_jobs(cls,spider, name,job_id, company, detail, industry,salary,area,vacant,date_posted):
        sql = 'INSERT INTO job (`theversion`,`name`,`job_id`, `company`, `detail`, `industry`,`salaryfrom`,`area`,`vacant`,`date_posted`) VALUES (1,%(name)s,%(job_id)s, %(company)s, %(detail)s, %(industry)s,%(salary)s, %(area)s, %(vacant)s, %(date_posted)s)'
        
        value = {
            'name': name,
            'job_id': job_id,
            'company': company,
            'detail': detail,
            'industry': industry,
            'salary': salary,
            'area': area,
            'vacant': vacant,
            'date_posted': date_posted.isoformat()
        }
#        spider.logger.info(value)
#        spider.LAW_LOG.append(value)
        try:
            cur.execute(sql, value)
            cnx.commit()
            for key,v in value.items():
                spider.logger.debug("done:"+key+":"+str(len(str(v))))
#                spider.LAW_LOG.append("done:"+key+":"+str(len(str(v))))
        except:
            pass
            for key,v in value.items():
                spider.logger.debug("error:"+key+":"+str(len(str(v))))
#                spider.LAW_LOG.append("error:"+key+":"+str(len(str(v))))

        


    @classmethod
    def select_name(cls, name_id):
        sql = "SELECT EXISTS(SELECT 1 FROM job WHERE name=%(name)s)"
        value = {
            'name': name_id
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]


