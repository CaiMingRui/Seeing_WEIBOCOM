# coding=utf-8

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


def login():
    """
    进行微博的手动登陆
    :return: null
    """
    browser.get("http://weibo.com/")
    while True:
        flag = raw_input('继续请输入Y，否则按任意键')
        if flag.upper() == 'Y':
            break


def get_search_page(keyword,page):
    print urllib.unquote(keyword)
    url = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%s&page=%d" % (keyword, page)
    print url
    browser.get(url)
    html = browser.page_source
    # key ="%s" %(keyword)
    save_html(keyword,page,html)


def save_html(key1,page,html):
    key=urllib.unquote(key1)
    if os.path.exists("/home/caimingrui/SJWJ/weibo/weibodate/html_moviename_page/"+key):
        print key + "_htmlpage is exists"
    else:
        os.mkdir("/home/caimingrui/SJWJ/weibo/weibodate/html_moviename_page/"+key)
    with open("/home/caimingrui/SJWJ/weibo/weibodate/html_moviename_page/"+key+'/'+str(page)+".txt", 'w') as f:
        f.write(html)


def get_user(key1,year):
    key = urllib.unquote(key1)
    for i in range(1,100):
        username=[]
        userid=[]
        userurl=[]
        with open("/home/caimingrui/SJWJ/weibo/weibodate/html_moviename_page/"+key+'/'+str(i)+".txt", 'r') as r:
            text=r.read()
            all = re.findall("<a href=\"https://weibo.cn/u/(\d*?)\" class=\"nk\">(.*?)<",text)
        for item in all:
            username.append(item[1])
            userid.append(item[0])
        for a in userid:
            if (a!= ''):
                x = "https://weibo.cn/u/"+str(a)
                print x
                userurl.append(x)
        save_name_url(username,userurl,key,i,year)

def save_name_url(username,userurl,key1,i,year):
    key = urllib.unquote(key1)
    if os.path.exists("/home/caimingrui/SJWJ/weibo/weibodate/user_url/"+str(year)):
        print str(year) + "page is exists"
    else:
        os.mkdir("/home/caimingrui/SJWJ/weibo/weibodate/user_url/"+str(year))

    if os.path.exists("/home/caimingrui/SJWJ/weibo/weibodate/user_url/"+str(year)+'/'+key):
        print key + "user_url is exists"
    else:
        os.mkdir("/home/caimingrui/SJWJ/weibo/weibodate/user_url/"+str(year)+'/'+key)
    with open("/home/caimingrui/SJWJ/weibo/weibodate/user_url/"+str(year)+'/'+key+'/'+str(i)+".txt",'a') as f:
        for url in userurl:
            f.write("[userurl]:"+url+'\n')
            f.write("[username]:"+username[userurl.index(url)]+'\n')
            f.write("----------------------------------------------------"+'\n')

if __name__ == '__main__':
    login()
    for year in range(2017,2018):
        movie_list = []
        with open("/home/caimingrui/SJWJ/weibo/weibodate/movie_time_name/"+str(year)+"/"+str(year)+'.txt','r') as r:
            moviename=r.read().split('\n')
            for movie in moviename:
                movie1 = urllib.quote(movie)
                movie_list.append(movie1)
    # print movie_list
        for keyword in movie_list:
            print "movie name", urllib.unquote(keyword)
            if os.path.exists("/home/caimingrui/SJWJ/weibo/weibodate/user_url/"+str(year)+'/'+urllib.unquote(keyword)+"/"+"99.txt"):
                print urllib.unquote(keyword)+"is exists,pass"
                continue
            else:
                for page in range(1,100):
                    t=random.random()
                    t1=10*t
                    time.sleep(t1)
                    get_search_page(keyword, page)
            if os.path.exists("/home/caimingrui/SJWJ/weibo/weibodate/user_url/"+str(year)+'/' + urllib.unquote(keyword) + "/" + "99.txt"):
                continue
            else:
                get_user(keyword,year)

