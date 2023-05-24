#coding=utf-8
import smtplib
from email.mime.text import MIMEText
import datetime
import logger
SendEmail = logger.getLogger('SendEmail')
#XHUBSCKLCONHXQZG
import time

class SendMail():
    def __init__(self, mail_host='smtp.163.com' , port=465):
        self.mail_host = mail_host
        self.port = port
        self.smtpObj = None
    def setupSmtp(self, mail_user, mail_pass):
        try:
            self.smtpObj = smtplib.SMTP_SSL(host=self.mail_host) 
            self.smtpObj.connect(host=self.mail_host,port=self.port)
            #smtpObj.starttls()
            self.smtpObj.login(mail_user,mail_pass) 
            SendEmail.info('Email login successful...')
            
        except Exception as e:
            SendEmail.error('Email login failed...')
            SendEmail.error(e)
    
    def sendMail(self, title, content, mail_user, mail_pass, receivers=[]):
        self.smtpObj = None
        n = 0
        while not self.smtpObj and n<10:
            self.setupSmtp(mail_user, mail_pass)
            n += 1
            time.sleep(5)
        sender = mail_user
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = title
        message['from'] = sender
        for receiver in receivers:
            message['to'] = receiver
            flag = False
            n = 0
            while not flag and n < 10:
                try:
                    self.smtpObj.sendmail(sender,receiver,message.as_string())
                    flag = True
                    SendEmail.info('Send success...')
                except Exception as e:
                    SendEmail.error('Send Failed...')
                    SendEmail.error(e) 
                    n += 1
                    time.sleep(5)
    
    def getTimeStamp(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')    
    
if __name__ == '__main__':
    sendmail = SendMail()
    sendmail.sendMail("有内鬼", "终止交易", "xxxx@163.com", "XHUBSCKLCONHXQZG",receivers=["yyyyy@qq.com"])