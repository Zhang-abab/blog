
import pymysql
from time import sleep
import os
dbhost = 'mysql'
dbuser = os.environ.get('POSTGRES_USER')
dbpasswd = os.environ.get('POSTGRES_PASSWORD')
dbname = os.environ.get('POSTGRES_NAME')
# 打开数据库连接
while True:
    try:
        db = pymysql.connect(host=dbhost, user=dbuser, password=dbpasswd, database=dbname)
        break
    except Exception as ex:
        print("暂未发现数据库")
        sleep(5)
print("数据库服务器在线，正在尝试连接.......")
while True:
    try:
        db = pymysql.connect(host=dbhost, user=dbuser, password=dbpasswd, database=dbname)
        break
    except Exception as ex:
        print("数据库未连接成功")
        sleep(5)
print("服务器连接成功 ：）")