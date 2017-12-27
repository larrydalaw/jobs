# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    id = scrapy.Field()
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
    name = scrapy.Field()
    score = scrapy.Field()
    movie_id = scrapy.Field()
    category=scrapy.Field()
    director = scrapy.Field()
    scriptwriter = scrapy.Field()
    movie_category = scrapy.Field()
    area = scrapy.Field()
    language = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    byname = scrapy.Field()
    '''