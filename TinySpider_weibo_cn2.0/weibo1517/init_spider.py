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

def init_sys(str_conf_fp):
    if(os.path.exists(str_conf_fp)):
        dom = xml.dom.minidom.parse(str_conf_fp)
        root=dom.documentElement
        dict["ReadMname"] = root.getElementsByTagName('ReadMname')[0]
        dict["SaveMname"] = root.getElementsByTagName('SaveMname')[0]
        dict["movie_html_page"] = root.getElementsByTagName('movie_html_page')[0]
        dict["save_Name_url"] = root.getElementsByTagName('save_Name_url')[0]
        dict["save_userpage"] = root.getElementsByTagName('save_userpage')[0]
    return dict