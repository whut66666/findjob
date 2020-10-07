# -*- codeing = utf-8 -*-
# @Time :  2020/9/27 15:22
# @Author : LiJunChao
# @File : testSqlite.py
# @SoftWare : PyCharm

import sqlite3

conn = sqlite3.connect("test.db")
print("成功打开数据库")
c = conn.cursor()   #获取游标

sql = ""

c.execute(sql)  #执行sql语句
c.commit()      #提交数据库操作
conn.close()    #关闭

print("成功建表")