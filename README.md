## 房价实时监控并推送

本项目开发之初是由于女朋友对于房子的渴望，促使我不得不想到一种比较智能的方式去获取某些地区的房价信息的波动情况。项目本身简单易行，本项目运行简单，通过短信直接将房价的波动推送到手机端。

### 运行
运行环境  
python 3.10  
------  
cron任务，定期触发执行推送  
service crond stop  
定时执行 crontab -e  
45 11 * * * bash /root/PriceMonitor/monitor.sh  
service crond start

### 后记
不断推动自己努力变强吧