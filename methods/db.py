#!/usr/bin/env python
#coding=utf-8

import MySQLdb

def db_conn():
  conn = MySQLdb.connect(host='192.168.20.193',user='wangpei',passwd='123456',db='test',port=3306,charset='utf8')
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

