from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import sys
sys.path.append("..")
import logger

class IMonitorBrowser(object):
    def __init__(self, browser_name, driver, logger_name, config_path=None):
        self.monitor = logger.getLogger(logger_name)
        self.browser_name = browser_name 
        self.driver = driver
        self.browser = None
        
    def getBrowser(self):
        return self.browser
    
    def initializeDriver(self):
        print('initializeDriver: create a '+browser_name+' driver')
        google_driver = self.driver
        if self.browser_name =='google':
            c_service = Service(google_driver)
            c_service.command_line_args()
            c_service.start()
        
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            self.browser = webdriver.Chrome(executable_path=google_driver,chrome_options=options)
            
    def login(browser, url, user_name='', passwd=''):
        pass
    
    def getHtml(self, url):
        #html = "https://ip.jiangxianli.com/?page=2"
        browser.get(html)
        html = browser.page_source
            