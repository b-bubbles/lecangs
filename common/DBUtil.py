#!/usr/bin/python
# coding=UTF-8


import pymysql

from common import tools

class DBUtil(object):
    connection=None
        
    @classmethod    
    def get_connection(cls,section='mysql_loctek'): 
        if cls.connection:
            return cls.connection
        try:
            db_info = tools.get_conf(section)
            host = db_info["host"]
            port = db_info["port"]
            user = db_info["user"]
            password = db_info["password"]
            database = db_info["database"]
            
            cls.connection = pymysql.connect(host=host, port=int(port), user=user, password=password,
                               database=database)
            return cls.connection
        except Exception as e:
            print("unable to connect to database,reason: %s" % e)


if __name__ == "__main__":
    DBUtil.connection=None
    conn=DBUtil.get_connection()
    cursor=conn.cursor()
    sql='select * from sys_user;'
    affected_rows=cursor.execute(sql)
    while True:
        data=cursor.fetchone()
        if data == None:
            break
        print(data)



