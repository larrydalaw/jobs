# -*- coding: utf-8 -*-

import re
from jobs import settings
import random
import scrapy #导入scrapy包
from bs4 import BeautifulSoup
from scrapy.http import Request , FormRequest##一个单独的request的模块，需要跟进URL的时候，需要用它
from jobs.items import JobsItem ##这是我定义的需要保存的字段，（导入dingdian项目中，items文件中的DingdianItem类）
from jobs.mysqlpipelines.sql import Sql#sql connection
import time
import datetime 
#from scrapy.log import logger
from time import strftime
from datetime import timedelta
from datetime import datetime, date
from scrapy.selector import HtmlXPathSelector

from selenium import webdriver
from scrapy.spiders import BaseSpider
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException 

class JobspiderSpider(BaseSpider):
    '''In each callback ensure that proxy /really/ returned your target page by checking for site logo or some other significant element. If not - retry request with dont_filter=True

if not hxs.select('//get/site/logo'):
    yield Request(url=response.url, dont_filter=True)
    '''

    name = 'jobspider'
    driver = None
    jobcount=0 
    jobpcount=0
    
    urldata = "&ID=&SortBy=&from=&start="+str(jobcount)
    urlpdata = "&ID=&SortBy=&from=&start="
    @classmethod
    def update_jobcount(cls, jc):
        JobspiderSpider.jobcount = jc
    @classmethod
    def get_jobcount(cls):
        return JobspiderSpider.jobcount
    @classmethod
    def get_urldata(cls):
        return JobspiderSpider.urldata    
    def __init__(self, *args, **kwargs):
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/lib/node_modules/phantomjs-prebuilt/bin/phantomjs')
    
        super(JobspiderSpider, self).__init__(*args, **kwargs)
   
        self.start_urls = ['https://www.jobs.gov.hk']



    def get_headers(self):
        ua = random.choice(settings.USER_AGENTS)
        headers = {
            "User-Agent": ua #'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
            }
        return headers

    def start_requests(self):
        request = Request(url=self.start_urls[0], meta={'JS':True},callback=self.parse)

        yield request
        
    def parse(self, response):
        soup = BeautifulSoup(response.text,'lxml')
        for a in soup.find_all('a',href=True):
            if a['href'].find("lang=tc") >0:
                lang_url=(a['href'])
                
        yield Request(url = lang_url, meta={'JS':True},callback=self.parse_front)
        
        
    def parse_front (self, response):
        self.logger.info(self.driver.current_url)
        select = Select(self.driver.find_element_by_id("ctl00_uxSimpLocation"))
        select.select_by_visible_text("--全香港島--")
        self.driver.find_element_by_id("ctl00_uxSimSearch").click()
        yield Request(url=self.driver.current_url, dont_filter=False,callback=self.parse_list)
     
    def parse_list (self, response):   
        
        for i in range(0,20):
            
             joblist = self.driver.find_element_by_xpath("//div[@id='uxItemLink_"+ str(i+1)+"']/table/tbody/tr/td[2]")
             joblist.click()
             jobselems = joblist.find_elements_by_tag_name("span")
             job =JobsItem()
             
             job ['vacant'] = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_uxJobCard_uxNoOfVac").text
             job ['company'] = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_uxJobCard_uxCompany").text
             job ['name'] = jobselems[0].text
             job ['job_id'] = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_uxJobCard_uxOrdNo").text
             details = self.driver.find_element_by_xpath("//div[@id='ctl00_ContentPlaceHolder1_uxJobCard_uxJcard']/table[2]/tbody/tr[5]/td").text

             if (details is not None):
                 result =""
                 for i in range (0, len(details.split())):
                     result = ''.join([result, details.split()[i], ' '])
                 job ['detail'] =result
             saldig = jobselems[1].text.find("月薪")
             if saldig > 0 :
                 job ['salary'] = int(jobselems[1].text[1:7].replace(',',''))
             else: 
                 job['salary'] = int(jobselems[1].text[1:3].replace(',',''))
             job ['area'] = jobselems[2].text
             pdate = self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_uxJobCard_uxPostedDate").text
             job ['date_posted'] = date(int(pdate.split('/')[2]),int(pdate.split('/')[1]),int( pdate.split('/')[0]))
             self.logger.info(job)
             yield (job)
        JobspiderSpider.update_jobcount(JobspiderSpider.get_jobcount()+20)
        nexturl=None
        try:
            nexturl = self.driver.find_element_by_xpath("//span[@id='ctl00_ContentPlaceHolder1_uxPageNum']/a[6]").get_attribute('href')
            self.logger.debug(nexturl +": expected partial")
            nexturl=self.driver.current_url +self.get_urlpdata()+str(JobspiderSpider.get_jobcount())
            self.logger.debug(nexturl + ": expected with no")
            yield Request(nexturl, dont_filter=False,callback=self.parse_list)
        except:
            self.driver.quit()
            pass
        

        

           
    def waitForLoad(self, driver):

        elem = driver.find_element_by_tag_name("html")
 
        while True:

            try:
                element = WebDriverWait (driver, 30).until(
                   EC.title_contains('Interactive Employment Service of the Labour Department')
                   or EC.title_contains ('勞工處互動就業服務'))
            finally:
                return
            