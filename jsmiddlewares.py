from scrapy import signals
from scrapy.http import HtmlResponse
#from scrapy.utils.python import to_bytes
from selenium import webdriver

class SeleniumMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        spider.logger.debug("==\\\\]]]")
        if 'JS' in request.meta:

            request.meta['driver'] = spider.driver  # to access driver from response
            spider.driver.get(request.url)
            self.waitForLoad(spider.driver)
            body =(spider.driver.page_source.encode('utf-8'))  # body must be of type bytes 
            return HtmlResponse(spider.driver.current_url, body=body, encoding='utf-8', request=request)

            

    def spider_opened(self, spider):
        pass
    def spider_closed(self, spider):
        pass
    def waitForLoad(self, driver):

        elem = driver.find_element_by_tag_name("html")
 
        while True:

            try:
               element = WebDriverWait (driver, 30).until(
                   EC.title_contains('Interactive Employment Service of the Labour Department')
                   or EC.title_contains ('勞工處互動就業服務'))
            finally: return

