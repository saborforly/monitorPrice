#coding=utf-8
import pymysql
import logging
import pandas as pd
import logger
Sql = logger.getLogger('Sql')
from sshtunnel import SSHTunnelForwarder

class Sql_manager():
    def __init__(self, host = 'localhost', port = 8766, user ="root", password = "!QAZ2wsx3edc", database_name = 'eos_io_test_new'):
        self.host = host
        self.port = port
        self.user = user 
        self.password = password
        self.database_name = database_name
        self.db = None
        self.cursor = None
        self.server = None
    def connectSql(self):
        try:
            self.server = SSHTunnelForwarder(
                ssh_address_or_host=('47.110.138.194', 22), # 指定ssh登录的跳转机的address
                ssh_username='root', # 跳转机的用户
                ssh_password='liuyan;123', # 跳转机的密码
                remote_bind_address=('172.17.32.177', 3306))
            self.server.start()
            #self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.database_name, charset='utf8')
            #self.cursor = self.db.cursor()
            self.db = pymysql.connect(host='127.0.0.1 ', port=self.server.local_bind_port, user="root", password="123456", db="beike")
            self.cursor = self.db.cursor()            
            Sql.info('connect sql success...')
        except Exception as e:
            Sql.error('connect sql failed...')
            Sql.error(e)        
        
    def closeSql(self):
        self.server.close()
        self.cursor.close()
        self.db.close()
    
    def addQuotationsForStr(self, li):
        if isinstance(li, str):
            return '\'' + li + '\''
        if isinstance(li, list):
            for i, element in enumerate(li):
                if isinstance(element, str):
                    li[i] = '\'' + element + '\''
                else:
                    li[i] = str(element)
            return li
        else:
            return li
    
    def sqlInsert(self, table='', keys=[], values=[]):
        if not table:
            Sql.error('Please appoint table name')
            return False
        if len(keys) != len(values):
            Sql.error('len(keys) != len(values)')
            return False
        if len(keys) == 0:
            Sql.error('keys and values must not be empty')
            return False
        
        keys = ','.join(keys)
        values = ','.join(self.addQuotationsForStr(values))
    
        query = "INSERT INTO {}({}) VALUES({})"\
            .format(table, keys, values)
        Sql.info(query)
        #query INSERT INTO table (keys) VALUES(values)
        self.cursor.execute(query)
        self.db.commit()
        return True
    
    def sqlUpdate(self, table='', keys=[], values=[],
                  condition_keys=[], condition_values=[]):
        if not table:
            Sql.error('Please appoint table name')
            return False
        if len(condition_keys) != len(condition_values):
            Sql.error('len(condition_keys) != len(condition_values)')
            return False
        if len(keys) != len(values):
            Sql.error('len(keys) != len(values)')
            return False
        if len(condition_keys) == 0:
            Sql.error('condition_keys and condition_values must not be empty')
            return False
        if not keys:
            Sql.error('key must not be empty')
    
        query = "UPDATE {} SET ".format(table)
        values = self.addQuotationsForStr(values)
        query += ' , '.join([' '+keys[i]+'='+values[i] \
                             for i in range(len(keys))])
    
        condition_values = self.addQuotationsForStr(condition_values)
        query += ' WHERE '
        query += ' AND '.join([' '+condition_keys[i]+'='+condition_values[i] \
                               for i in range(len(condition_keys))])
        Sql.info(query)
        # condition_key1   tableKey
        # querry: UPDATE table SET key1=value1, key2=value2, WHERE condition_key1=condition_value1 AND condition_key2=condition_value2
        self.cursor.execute(query)
        self.db.commit()
    def sqlSelect(self,  table='', keys=['*'], condition_keys=[], condition_values=[], distinct=False, limit=False):
        if len(condition_keys) != len(condition_values):
            logging.error('len(condition_keys) != len(condition_values)')
            return False
        if len(keys) == 0:
            keys = ['*']

        query = "SELECT "
        if distinct:
            query +="DISTINCT "
        query += ','.join(keys)
        query += " FROM {}".format(table)

        if condition_keys:
            query += ' WHERE'
            condition_values = self.addQuotationsForStr(condition_values)
            query += ' AND '.join([' '+condition_keys[i]+'='+condition_values[i] \
                for i in range(len(condition_keys))])

        if limit:
            query += ' LIMIT '
            query += str(limit)

        logging.info(query)
        data = pd.read_sql(query, con=self.db)
        return data
    
if __name__ == '__main__':
    #spider = BeikeMonitorSpider()
    sql = Sql_manager(host='47.110.138.194 ', port=3306, user = "root", password="123456", 
                     database_name='beike')
    sql.connectSql()
    
    #sql.sqlInsert(table='Data', keys=['title','publish','year','position','roomType','area','totalPrice','unitPrice','follow','flood','toward'],
    #              values=['阿里', 2001, 2001, "杭州",'一室',51,200,70000,60,'高层','南'])
    item = sql.sqlSelect(table='Data', keys=['*'], condition_keys=['title'], 
                 condition_values=['阿'], distinct=False, 
                 limit=False)
    print(item.empty)
    
    #print(list(item.loc[0,:]))
    
    sql.closeSql()