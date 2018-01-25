# -*- coding:utf-8 -*-
from __future__ import division
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from xml.dom import minidom
import xml.dom.minidom
import re
import json
import datetime
import chardet
import os
import random
import urllib
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#task1 作为整个爬虫任务的第一部分，主要完成了获取电影的目标网址，获取了电影的评论，同时保存了电影的评论用户的链接
#task2 作为第二部分，主要是将扩充评论里的评论用户的链接获取下来，存到task3要用的用户url列表中
#task3 作为任务的第二部分，主要是通过task1获得的用户链接，去获取用户的三个主界面。

######################
#                    #
#       task3        #
#                    #
######################


browser = webdriver.Firefox()


def init_spider():
    login()
    return browser

def login():
    browser.get("http://weibo.com/")
    browser.maximize_window()
    try:
        WebDriverWait(browser,30,3).until(lambda browser:browser.find_element_by_xpath('//div[@class="info_list username"]/div/input[@id="loginname"]'))
        userBtn = browser.find_element_by_xpath('//div[@class="info_list username"]/div/input[@id="loginname"]')
        userBtn.click()
        userBtn.clear()
        time.sleep(2)
        passBtn = browser.find_element_by_xpath('//div[@class="info_list password"]/div/input[@type="password"]')
        passBtn.clear()
        passBtn.click()
        # ActionChains.move_to_element(userBtn).click()
        userBtn.send_keys("loginname")
        time.sleep(2)
        # ActionChains.move_to_element(passBtn).click()
        passBtn.send_keys("password")
        time.sleep(1)
        Btn=browser.find_element_by_xpath("//div[@class='info_list login_btn']/a/span[@node-type='submitStates']")
        ActionChains(browser).move_to_element(Btn).perform()
        Btn.click()
        WebDriverWait(browser, 30, 3).until(lambda browser: browser.find_element_by_xpath('//div[@class="WB_innerwrap"]/div[@class="nameBox"]'))
        print "----------------------------have been logined and try to get search page-----------------------"
        time.sleep(10*random.random())
    except Exception,r:
        print '*******************************login(loginname) fail******************************'
        print Exception,":",r
        print '*******************************login(loginname) fail******************************'

def load_req():
    years = os.listdir('./user_url_comments/')
    for year in years:
        files = os.listdir('./user_url_comments/'+str(year)+'/')
        for file in files:
            url_set = []
            name = file.replace(".json", "")
            with open('./user_url_comments/'+str(year)+'/'+file,'r') as r:
                textA = r.read()
                urlsA = re.findall("\[user_url\]\:(.*?)\[/user_url\]",textA)

            for a in urlsA:
                urlA = re.sub("\?refer_flag="+'\d+'+"_","",a)
                url_set.append(urlA)
            with open('./more_user_url_comments/'+str(year)+'/'+file,'r') as x:
                textB = x.read()
                urlsB = re.findall("\[user_url\]\:(.*?)\[/user_url\]", textB)
            for b in urlsB:
                urlB = re.sub("\?refer_flag="+'\d+'+"_","",b)
                url_set.append(urlB)
            url_qc = list(set(url_set))
            for url in url_qc:
                exec_spider(year, name, url)

def exec_spider(year,name,url):
    print "*******************************"+year,name+"************************************"
    print url
    if('/u' in url):
        id = re.findall("https\://weibo\.com/u/(\d+)",url)[0]
    else:
        id = re.findall("https\://weibo\.com/([\w]+)",url)[0]
    # if(os.path.exists("./movie_user/"+str(year))==False):
    #     os.mkdir("./movie_user/"+str(year)+"/")
    # with open("./movie_user/"+str(year)+"/"+name+".json",'a') as w:
    #     w.write(id+'\n')
    with open("./totle_user.json",'a+') as o:
        text = o.read()
        if(id in text):
            print "该用户已存在"
            return
        else:
            get_page(year,name,url,id)
            if (os.path.exists("./movie_user/" + str(year)) == False):
                os.mkdir("./movie_user/" + str(year) + "/")
            with open("./movie_user/" + str(year) + "/" + name + ".json", 'a') as w:
                w.write(id+'\n')
            o.write(id+'\n')
            print "登记"+name,str(id)+"成功"

def get_page(year,name,url,id):

    print "开始进入"+str(id),url
    browser.get(url)
    home={}
    follow={}
    info={}
    Wuser = {}
    Wuser["Uid"] = id
    WebDriverWait(browser, 30, 3).until(lambda browser:browser.find_element_by_xpath('//div[@class="PCD_counter"]/div[@class="WB_innerwrap"]/table[@class="tb_counter"]/tbody/tr/td/a[@class="t_link S_txt1"]'))
    print "进入主页..."
    time.sleep(random.random()+10*random.random())
    homepage = browser.page_source
    homeurl = browser.current_url
    Wuser["follow_num"] = browser.find_element_by_xpath("//a[contains(@href,'follow?from=page')]/strong").text
    Wuser["fans_num"] = browser.find_element_by_xpath("//a[contains(@href,'follow?relate=fans')]/strong").text
    Wuser["weibo_num"] = browser.find_element_by_xpath("//a[contains(@href,'home?from=page')]/strong").text
    if(id.isdigit()):
        Wuser["is_bigV"] = 'N'
    else:
        Wuser["is_bigV"] = 'Y'
    Wuser["repo_num"] = 0
    Wuser["comment_num"] = 0
    Wuser["like_num"] = 0
    repos = browser.find_elements_by_xpath("//div[@class='WB_feed WB_feed_v3 WB_feed_v4']/div[@class='WB_cardwrap WB_feed_type S_bg2 WB_feed_vipcover WB_feed_like ']/div[@class='WB_feed_handle']/div[@div='WB_handle']/ul/li[2]/a/span/span/span/em[2]")
    for r in repos:
        if(r.text.isdigit()):
            Wuser["repo_num"] = Wuser["repo_num"]+r.text
        else:
            Wuser["repo_num"] = Wuser["repo_num"]+0

    comments = browser.find_elements_by_xpath("//div[@class='WB_feed WB_feed_v3 WB_feed_v4']/div[@class='WB_cardwrap WB_feed_type S_bg2 WB_feed_vipcover WB_feed_like ']/div[@class='WB_feed_handle']/div[@div='WB_handle']/ul/li[3]/a/span/span/span/em[2]")
    for c in comments:
        if(c.text.isdigit()):
            Wuser["comment_num"] = Wuser["comment_num"]+c.text
        else:
            Wuser["comment_num"] = Wuser["comment_num"]+0

    like = browser.find_elements_by_xpath("//div[@class='WB_feed WB_feed_v3 WB_feed_v4']/div[@class='WB_cardwrap WB_feed_type S_bg2 WB_feed_vipcover WB_feed_like ']/div[@class='WB_feed_handle']/div[@div='WB_handle']/ul/li[4]/a/span/span/span/em[2]")
    for l in like:
        if(l.text.isdigit()):
            Wuser["like_num"] = Wuser["like_num"]+l.text
        else:
            Wuser["like_num"] = Wuser["like_num"]+0
    print "主页获取完毕..."
    infoBtn = browser.find_element_by_class_name('more_txt')
    infoBtn.click()
    WebDriverWait(browser, 30, 3).until(lambda browser:browser.find_element_by_xpath("//a[contains(@href,'follow?from=page')]"))
    print "进入资料页..."
    time.sleep(random.random()+10*random.random())
    infopage = browser.page_source
    infourl = browser.current_url
    print "资料页获取完毕..."
    followBtn = browser.find_element_by_xpath("//a[contains(@href,'follow?from=page')]")
    followBtn.click()
    WebDriverWait(browser, 30, 3).until(lambda browser:browser.find_element_by_xpath('//div[@class="WB_frame"]/div[@id="plc_main"]'))
    print "进入关注页..."
    time.sleep(random.random()+10*random.random())
    followpage = browser.page_source
    followurl = browser.current_url
    print "关注获取完毕..."
    home['page']=homepage
    home['url']=homeurl
    follow['page']=followpage
    follow['url']=followurl
    info['page']=infopage
    info['url']=infourl
    if not os.path.exists("./user_page/"+str(id)+"/"):
        os.mkdir("./user_page/"+str(id))
    with open("./user_page/"+str(id)+"/home.json",'w') as h:
        baby1 = json.dumps(home,ensure_ascii=False)
        h.write(baby1)
    with open("./user_page/"+str(id)+"/info.json",'w') as i:
        baby2 = json.dumps(info,ensure_ascii=False)
        i.write(baby2)
    with open("./user_page/"+str(id)+"/follow.json",'w') as f:
        baby3 = json.dumps(follow,ensure_ascii=False)
        f.write(baby3)

    with open("./weibo_user/"+str(id)+".json",'w') as hh:
        oo = json.dumps(Wuser,ensure_ascii=False)
        hh.write(oo)

    print id,"写入完毕"


if __name__ == '__main__':
    # try:
    init_spider()
    load_req()
    # except Exception,error:
    #     print Exception,":",error
    #     browser.quit()
