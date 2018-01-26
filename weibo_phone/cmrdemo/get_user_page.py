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

def get_from_txt(n,m):
    for year in range(n,m):
        with open("/home/caimingrui/SJWJ/weibo/weibodate/movie_time_name/"+str(year)+"/"+str(year)+'.txt','r') as r:
            moviename=r.read().split('\n')
        for keyword in moviename:
            namelist=[]
            urllist=[]
            for i in range(1,100):
                if os.path.getsize("/home/caimingrui/SJWJ/weibo/weibodate/user_url/" + str(year)+'/'+ keyword + '/' + str(i) + ".txt"):
                    # print "-----已读取文件"+keyword+"_"+str(i)+"------"
                    with open("/home/caimingrui/SJWJ/weibo/weibodate/user_url/" + str(year)+'/'+ keyword + '/' + str(i) + ".txt", 'r') as f:
                        text = f.read()
                        # name=re.findall("",text)
                        # url=re.findall("",text)
                        pattern=re.compile("userurl\]:(.*?)\\n.*?username\]:(.*?)\\n",re.S)
                        list=re.findall(pattern,text)
                        for x in list:
                            namelist.append(x[1])
                            urllist.append(x[0])
            get_page(namelist,urllist,year,keyword)

def get_page(namelist,urllist,year,keyword):
    if os.path.exists("/home/caimingrui/SJWJ/weibo/weibodate/user_page/"+str(year)):
        print "page" + str(year) + "is exists"
    else:
        os.mkdir("/home/caimingrui/SJWJ/weibo/weibodate/user_page/" + str(year))

    if os.path.exists("/home/caimingrui/SJWJ/weibo/weibodate/user_page/"+str(year)+"/"+keyword):
        print "page" + keyword + "is exists"
    else:
        os.mkdir("/home/caimingrui/SJWJ/weibo/weibodate/user_page/" + str(year)+"/"+keyword)

    for name in namelist:
        if os.path.exists("/home/caimingrui/SJWJ/weibo/weibodate/user_page/"+ str(year)+"/"+keyword+'/'+name):
            print "user"+name+"is exists"
            break
        else:
            os.mkdir("/home/caimingrui/SJWJ/weibo/weibodate/user_page/"+ str(year)+"/"+keyword+'/'+name)
        main_url = urllist[namelist.index(name)]
        message_url = urllist[namelist.index(name)].replace('/u/','/')+urllib.quote("/info")
        follow_url = urllist[namelist.index(name)].replace('/u/','/')+urllib.quote("/follow")
        browser.get(main_url)
        print main_url
        print "获取"+name+"主页"
        main_page = browser.page_source
        print message_url
        print "获取"+name+"资料"
        t = 5*random.random()
        time.sleep(t)
        browser.get(message_url)
        message_page = browser.page_source
        print follow_url
        print "获取"+name+"关注"
        t1 = 6*random.random()
        time.sleep(t1)
        browser.get(follow_url)
        follow_page = browser.page_source

        with open("/home/caimingrui/SJWJ/weibo/weibodate/user_page/"+ str(year)+"/"+keyword+'/'+name+"/"+"main.txt",'w') as f:
            f.write(main_page)
        with open("/home/caimingrui/SJWJ/weibo/weibodate/user_page/" + str(year)+"/"+keyword+'/'+name + "/" + "message.txt", 'w') as j:
            j.write(message_page)
        with open("/home/caimingrui/SJWJ/weibo/weibodate/user_page/" + str(year)+"/"+keyword+'/'+name + "/" + "follow.txt", 'w') as l:
            l.write(follow_page)

if __name__ == '__main__':
    login()
    get_from_txt(2017,2018)