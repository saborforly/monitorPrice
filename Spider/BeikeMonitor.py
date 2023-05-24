#coding=utf-8
import urllib
import sys
sys.path.append("..")
from bs4 import BeautifulSoup
import requests
import re
from Spider.IMonitorSpider import IMonitorSpider


class BeikeMonitorSpider(IMonitorSpider):
    def __init__(self, logger_name='BeikeMonitorSpider', config_path=None):
        super(BeikeMonitorSpider,self).__init__(logger_name, config_path)
        self.url = "https://sh.ke.com/ershoufang/"
        
        #allPrice='p1', area="nha0", house_type="l2"
        #拼接网页
        self.places =["changning/","putuo/"]
        self.area = "a2a3"  #50m3-90m3
        self.data = []
        
    def spiderData(self):
        allUrl = self.getAllUrl()
        for url in allUrl:
            pageData = self.getItem(url)
            #install SQL
        return self.data
                
    def getAllUrl(self):
        allUrl=[]
        
        allIniPage = []
        for place in self.places:
            url = self.url+place
            allIniPage.append(url)
        for page in allIniPage:
            url = page + self.area
            allPageNum = self.getAllPageNum(url)
            for i in range(1, allPageNum+1):
                newUrl = page+"pg"+str(i)+self.area
                allUrl.append(newUrl)
        return allUrl
                
        
    def getAllPageNum(self, url):
        status, page = self.getHtmlText(url)
        soup = BeautifulSoup(page)
        page_data = soup.find('div','contentBottom clear').find("div", "page-box house-lst-page-box").attrs["page-data"]
        #print(page_data)
        allPageNum = eval(page_data)["totalPage"]
        allPageNum = int(allPageNum)
        return allPageNum
        
    def getItem(self, url):
        status, page = self.getHtmlText(url)
        #print(page)
        #print(status)
        soup = BeautifulSoup(page)
        #<div class="viewbox"><div class="content"><span id="color_999">性别：女
        text = soup.find('ul','sellListContent').find_all("li", "clear")
        
        
        for i in text:
            td_all = i.find('div', "info clear")
            
            td_dic = {}
            #title
            title = td_all.find("div", "title").find('a')
            td_dic['url'] = str(title.attrs['href'])
            td_dic['title'] = str(title.get_text().replace("\'", "").replace("\"", ""))  #== print(title.attrs["title"])
            address = td_all.find("div", "address")
            
            #position
            position = address.find("div", "flood").find("a").get_text().replace("\'", "").replace("\"", "")
            td_dic['position'] = str(position)
            
            #houseInfor
            houseInfo = address.find("div", "houseInfo").get_text().replace("\n", "").replace(" ","").replace("\'", "").replace("\"", "")
            houseInfo = houseInfo.split('|')
            for info in houseInfo:
                if "楼层" in info:
                    td_dic['flood'] = str(info)
                if "年" in info:
                    match = re.search(r'(\d+).*', info)                   
                    td_dic['year'] = int(match.group(1))
                if "室" in info:
                    td_dic['roomType'] = str(info)
                if "平米" in info:
                    match = re.search(r'(\d+).*', info)     
                    td_dic['area'] = float(match.group(1))
                if "南" or "北" or "西" or "东" in info:
                    td_dic['toward'] = str(info)
            
            #price
            priceInfo = address.find("div", "priceInfo")
            totalPrice = priceInfo.find("div", "totalPrice").find("span").get_text()
            unitPrice = priceInfo.find("div", "unitPrice").attrs["data-price"]
            td_dic["totalPrice"] = float(totalPrice)
            td_dic["unitPrice"] = float(unitPrice)
            
            #follow
            followInfo = address.find("div", "followInfo").get_text().replace("\n", "").replace(" ","").split("/")
            for info in followInfo:
                if "关注" in info :
                    follow = re.search(r'(\d+).*', info)
                    td_dic["follow"] = int(match.group(1))
                if "发布" in info :
                    publish = re.match(r'\d', info)
                    day = 0
                    if "年" in info:
                        match = re.search(r'(?P<year>\d+)年.*', info)
                        day += int(match.group('year'))*12*30
                    if "月" in info:
                        match = re.search(r'(?P<month>\d+)月.*', info)
                        day += int(match.group('month'))*30
                    if "日" in info:
                        match = re.search(r'(?P<day>\d+)日.*', info)
                        day += int(match.group('day'))
                    td_dic["publish"] = day
            #print(td_dic)
            self.data.append(td_dic) 
        
        
if __name__ == "__main__":
    monitor = BeikeMonitorSpider()
    monitor.spiderData()
        
    
        