#encoding: utf-8
import os
import pymysql
pymysql.install_as_MySQLdb()

DEBUG = True

user ='root'
password = '1234'
host = '127.0.0.1'
port = '3306'
dbname = 'zhiliao'

DB_URI="mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8".format(user,password,host,port,dbname)
SQLALCHEMY_DATABASE_URI=DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS=False