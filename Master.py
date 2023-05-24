#coding=utf-8
from  SendMail import SendEmail
from sql_operations import Sql_manager
from Spider.BeikeMonitor import BeikeMonitorSpider
from SendMail import SendMail 

if __name__ == '__main__':
    spider = BeikeMonitorSpider()
    pageData = spider.spiderData()
    
    sql = Sql_manager(host='47.110.138.194 ', port=3306, user = "root", password="123456", database_name='beike')
    sql.connectSql()
    #sql.sqlInsert(table='Data', keys=['follow', 'unitPrice', 'toward', 'title', 'area', 'flood', 'year', 'roomType', 'publish', 'position', 'totalPrice'],
    #              values=[54, 57651.0, '南', '本周必卖，精装修，中间楼层，一梯两户，全明户型', 54.0, '中楼层(共6层)', 2009, '1室1厅', 120, '新泾家苑', 315.0])
    
    sendmail = SendMail()
    #sendmail.sendMail(title, content, "saborforly@163.com", "XHUBSCKLCONHXQZG")
    
    for item in pageData:
        keys = list()
        values = list()
        sel_keys = []
        sel_values = []
        for key, value in item.items():
            if key == "url":
                sel_keys.append(key)
                sel_values.append(value)
            keys.append(key)
            values.append(value)
           
        #正确 INSERT INTO Data(follow,unitPrice,toward,title,area,flood,year,roomType,publish,position,totalPrice) VALUES(54,57651.0,'南','本周必卖，精装修，中间楼层，一梯两户，全明户型',54.0,'中楼层(共6层)',2009,'1室1厅',120,'新泾家苑',315.0)
        result = sql.sqlSelect(table='Data', keys=['*'], condition_keys=sel_keys, condition_values=list(sel_values))
        
        content = "房间描述："+item["title"]+"\n"
        content += "类型： "+str(item["roomType"])+"\n"
        content += "总价："+str(item["totalPrice"]) + " 万元"+"\n"
        content += "每平米价格： "+str(item["unitPrice"])+" 元/平米"+"\n"
        content += "房间面积： "+str(item["area"])+" 平方米"+"\n"
        content += "房间朝向： "+str(item["toward"])+"\n"
        content += "位置： "+str(item["position"])+"\n"
        content += "楼层： "+str(item["flood"])+"\n"
        content += "发布时间： "+str(item["publish"])+"天前"+"\n"
        content += "详细信息： "+str(item["url"])+"\n"        
        if(result.empty):
            message = "有新房发布"+"\n" + content
            sendmail.sendMail("贝壳选房", message, "abc@163.com", "xxxxxx",receivers=["abc@qq.com","def@163.com"])
            sql.sqlInsert(table='Data', keys=keys, values= list(values))
        else:
            print(result["totalPrice"][0], float(item["totalPrice"]))
            if result["totalPrice"][0] < float(item["totalPrice"]):
                leave =   float(item["totalPrice"]) - result["totalPrice"][0]
                message = "该房价涨了：" +str(leave)+ "万元" +"\n" + content
                sendmail.sendMail("贝壳选房", message, "abc@163.com", "xxxxxx",receivers=["abc@qq.com","def@163.com"])
                sql.sqlUpdate(table='Data', keys=keys, values=list(values), condition_keys=sel_keys, condition_values=sel_values)
            elif result["totalPrice"][0] > float(item["totalPrice"]):
                leave = result["totalPrice"][0] -  float(item["totalPrice"])
                message = "该房价降了：" +str(leave)+ "万元" +"\n" + content
                sendmail.sendMail("贝壳选房", message, "abc@163.com", "xxxxxx",receivers=["abc@qq.com","def@163.com"])
                sql.sqlUpdate(table='Data', keys=keys, values=list(values), condition_keys=sel_keys, condition_values=sel_values)
            
    sql.closeSql()
                
        
        
        