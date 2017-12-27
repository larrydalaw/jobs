#encoding=utf-8

import MySQLdb

import re
from jobs import settings
import random
#import scrapy #导入scrapy包
from bs4 import BeautifulSoup
#from scrapy.http import Request , FormRequest##一个单独的request的模块，需要跟进URL的时候，需要用它
from jobs.items import JobsItem ##这是我定义的需要保存的字段，（导入dingdian项目中，items文件中的DingdianItem类）
from jobs.mysqlpipelines.sql import Sql#sql connection
from urllib.parse import urlparse 
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException 
import logging
import datetime 

import sys
import os

class DJob():
    def __init__(self):
        bash_url = 'https://www.jobs.gov.hk'    
        self.db = MySQLdb.connect(host='127.0.0.1', user="pandalaw", passwd="LL456852samysql", db="jobs")
        # 获取操作游标
        self.cursor = self.db.cursor()



    def start_parse(self):

        driver = webdriver.PhantomJS(executable_path='/usr/local/lib/node_modules/phantomjs-prebuilt/bin/phantomjs')
        driver.get(bash_url)
        self.waitForLoad(driver)
        theresponse = driver.page_source
        soup = BeautifulSoup(theresponse,'lxml')
        for a in soup.find_all('a',href=True):
            if a['href'].find("lang=tc") >0:
                lang_url=(a['href'])
        driver.get(lang_url)
        select = Select(driver.find_element_by_id("ctl00_uxSimpLocation"))
        select.select_by_visible_text("--全香港島--")
        driver.find_element_by_id("ctl00_uxSimSearch").click()
        self.logger.log(logging.INFO, "time" +str(datetime.datetime.now()))
        for i in range(0,20):
             joblist = driver.find_element_by_xpath("//div[@id='uxItemLink_"+ str(i+1)+"']/table/tbody/tr/td[2]")
             self.logger.log(logging.INFO, BeautifulSoup(joblist.get_attribute('innerHTML'), 'lxml'))
             joblist.click()
             jobselems = joblist.find_elements_by_tag_name("span")
             for j in jobselems:
                 print(BeautifulSoup(j.get_attribute('innerHTML'),'lxml').prettify())
             job =JobsItem()
             
             job ['vacant'] = driver.find_element_by_id("ctl00_ContentPlaceHolder1_uxJobCard_uxNoOfVac").text
             job ['company'] = driver.find_element_by_id("ctl00_ContentPlaceHolder1_uxJobCard_uxCompany").text
             job ['name'] = jobselems[0].text
             job ['job_id'] = driver.find_element_by_id("ctl00_ContentPlaceHolder1_uxJobCard_uxOrdNo").text
             job ['detail'] = driver.find_element_by_xpath("//div[@id='ctl00_ContentPlaceHolder1_uxJobCard_uxJcard']/table[2]/tbody/tr[5]/td").text
             job ['salary'] = jobselems[1].text
             job ['area'] = jobselems[2].text
             job ['date_posted'] = driver.find_element_by_id("ctl00_ContentPlaceHolder1_uxJobCard_uxPostedDate").text
             self.logger.log(logging.INFO, job)
             savetodb(job)
        pass
    
    def savetodb(JobsItem):
        item = JobsItem
        try:
            result = self.cursor.execute("insert into  job(id, job_name, job_id, company, detail, industry, salaryfrom, salaryto, area, vacant, date_posted) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10]])
            self.db.commit()
            print(result)
        except Exception as e:
            self.db.rollback()
            print('失败')

        # 关闭连接，释放资源
        self.db.close()
        pass
        
    def waitForLoad(self, driver):
        elem = driver.find_element_by_tag_name("html")
        count = 0 
        while True:
            count+=1
            if count >20 :
                self.logger.log(logging.INFO, "time out")
                return
            time.sleep(.5)
            try:
                elem == driver.find_element_by_tag_name("html")
            except StaleElementReferenceException:
                return

if __name__ == "__main__":
    djob = DJob()
    djob.start_parse()