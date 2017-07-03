#!/usr/bin/env python
#coding=utf-8

import MySQLdb

def db_conn():
  conn = MySQLdb.connect(host='192.168.20.193',user='wangpei',passwd='123456',db='test',port=3306,charset='utf8mb4')
  return conn

def select_table(table,column,condition,value):
  conn = db_conn()
  cur = conn.cursor()
  sql = "select {0} from {1} where {2} = '{3}'".format(column,table,condition,value)
  cur.execute(sql)
  lines = cur.fetchall()
  cur.close()
  conn.close()
  return lines

def select_columns(table,column):
  conn = db_conn()
  cur = conn.cursor()
  sql = "select {0} from {1}".format(column,table)
  cur.execute(sql)
  lines = cur.fetchall()
  cur.close()
  conn.close()
  return lines

def select_blog_title(table,column):
  conn = db_conn()
  cur = conn.cursor()
  sql = "select {0} from {1}".format(column,table)
  cur.execute(sql)
  lines = cur.fetchall()
  cur.close()
  conn.close()
  return lines

def select_blog_content(table,column):
  conn = db_conn()
  cur = conn.cursor()
  sql = "select {0} from {1}".format(column,table)
  cur.execute(sql)
  lines = cur.fetchall()
  cur.close()
  conn.close()
  return lines

def add_blog_content(id,user_id,user_name,title,content,created_at):
  conn = db_conn()
  cur = conn.cursor()
  sql = "insert into blogs(id,user_id,user_name,title,content,created_at) values ({0},{1},'{2}','{3}','{4}','{5}')".format(id,user_id,user_name,title,content,created_at)
  cur.execute(sql)
  cur.close()
  conn.commit()
  conn.close()

def select_content_byid(table,column,condition,value):
  conn = db_conn()
  cur = conn.cursor()
  sql = "select {0} from {1} where {2} = '{3}'".format(column,table,condition,value)
  cur.execute(sql)
  lines = cur.fetchall()
  cur.close()
  conn.close()
  return lines

def update_blog_content(id,user_id,user_name,title,content):
  conn = db_conn()
  cur = conn.cursor()
  sql = "update blogs set user_id={0},user_name='{1}',title='{2}',content='{3}' where id={4}".format(user_id,user_name,title,content,id)
  cur.execute(sql)
  cur.close()
  conn.commit()
  conn.close()

