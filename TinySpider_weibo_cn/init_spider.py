#coding=utf-8

from __future__ import division
from selenium import webdriver
import re
import datetime
import chardet
import urllib
import os
import random
import time
import sys
reload(sys)

sys.setdefaultencoding('utf-8')
browser = webdriver.Chrome(executable_path='/home/caimingrui/geckodriver')  # 启动浏览器

def init_spider(dict_args):
    login(dict_args)
    return browser


def login(dict_args):
    """
    进行微博的手动登陆
    :return: null
    """
    browser.get("http://weibo.com/")
    while True:
        flag = raw_input('继续请输入Y，否则按任意键')
        if flag.upper() == 'Y':
            break

