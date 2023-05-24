#coding=utf-8
import urllib
from bs4 import BeautifulSoup
import requests
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
import sys
sys.path.append("..")
import logger
useProxy = logger.getLogger('useProxy')

class GetProxy():
    def __init__(self, proxyHub="https://ip.jiangxianli.com/"):
        self.proxyHub = proxyHub
        self.proxyInfo = []
        self.effectProxy = []
        
    def getEffectProxy(self):
        return self.effectProxy
    
    def getHtml(self, url, proxy=None):
        # get web
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        #requests.adapters.DEFAULT_RETRIES = 5
        try:
            if proxy!=None:
                proxies = {
                 'http': "http://"+proxy,
                'https': "https://"+proxy,}
                req = requests.get(url=url, headers=headers, proxies=proxies,timeout=10)
            else:
                req = requests.get(url=url, headers=headers)
            status_code = req.status_code
            page = req.text
            return status_code, page
        except Exception as e:
            useProxy.error("getHtml failed")
            useProxy.error("failed message"+e)
    
    def check_proxy(self):
        #代理是否有效
        url='https://cn.bing.com/'
    
        for ip_dic in self.proxyInfo:
            try:
                proxy = ip_dic['ip']+":"+ip_dic['port']
                status, page = self.getHtml(url, proxy)
                if status == 200:
                    useProxy.info('可用代理'+proxy)
                    self.effectProxy.append(proxy)
            except Exception as e:
                useProxy.error('failed connect')
                useProxy.error(e)            
    
    def get_proxy_info(self, url):
        status, page = self.getHtml(url)
        soup = BeautifulSoup(page)
        #<div class="viewbox"><div class="content"><span id="color_999">性别：女
        try:
            text = soup.find('div','layui-form').find('table','layui-table').find('tbody').find_all('tr')
        except Exception as e:
            useProxy.error('failed find proxyInfo')
        id_key = ['ip', 'port', 'hid', 'type', 'addr', 'country']
        for i in text:
            td_all = i.find_all('td')
            if len(td_all)==0 :
                continue
            td_dic = {}
            for i,td in enumerate(td_all):
                if i>5: break
                td_dic[id_key[i]] = td.get_text()
            self.proxyInfo.append(td_dic)
    
    def do_scan_proxyHub(self):
        #查看有多少页, 该网页使用script 隐藏了这个信息
        #soup.find(name=None, attrs={}, recursive=True, text=None)
        #status, page = self.getHtml(self.proxyHub)
        #print(page)
        #soup = BeautifulSoup(page)    
        #text = soup.find('div',id='paginate')
        #print(text) 可以打印
        #page_count = soup.find('span', attrs={"class":'layui-laypage-count'})
        
        for i in range(1):
            url = self.proxyHub +'?page='+str(i)
            data = self.get_proxy_info(url)
            self.proxyInfo.append(data)
        
        
if __name__ == '__main__':
    proxy = GetProxy()
    proxy.do_scan_proxyHub()
    proxy.check_proxy()
    print(proxy.getEffectProxy())
    
    #chromeOptions = webdriver.ChromeOptions()
    #chromeOptions.add_argument('--headless')
    #browser =webdriver.Chrome(executable_path =r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",chrome_options =chromeOptions)
    #browser.get("https://ip.jiangxianli.com/?page=2")
    #html = browser.page_source
    #print(html)