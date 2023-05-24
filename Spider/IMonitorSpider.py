import sys
sys.path.append("..")
import logger
import urllib
import requests

class IMonitorSpider(object):
    def __init__(self, logger_name, config_path=None):
        self.monitor = logger.getLogger(logger_name)
        
    def getHtmlText(self, url, proxy=None):
        # »ñÈ¡ÍøÒ³ÄÚÈÝ
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        requests.adapters.DEFAULT_RETRIES = 5
        try:
            if proxy!=None:
                proxies = {
                'http': "http://"+proxy,
                'https': "https://"+proxy,
                }
                req = requests.get(url=url, headers=headers, proxies=proxies,timeout=1)
        
            else:
                req = requests.get(url=url, headers=headers)
            status_code = req.status_code
            page = req.text
            self.monitor.info("get Html")
            return status_code, page
        except Exception as e:
            print(e)
            self.monitor.error("getHtml failed")