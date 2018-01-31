# -*- coding:utf-8 -*-
from __future__ import division
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from xml.dom import minidom
import xml.dom.minidom
import re
import json
import login
import send_mail
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
Downloadpage = '-1'


def init_spider():
    login.login(browser)
    return browser



def load_req():
    years = os.listdir('./user_url_comments/')
    for year in years:
        with open('./CheckDate/task3CK/yearcheck.txt', 'a+') as ycheck:
            all = ycheck.readlines()
            if str(year)+'\n' in all:
                print year,'pass'
                continue
        files = os.listdir('./user_url_comments/'+str(year)+'/')
        for file in files:
            with open('./CheckDate/task3CK/'+str(year)+'.txt','a+') as fcheck:
                all = fcheck.readlines()
                if file+'\n' in all:
                    print file,'pass'
                    continue
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
                exec_spider(year, name, url.replace('http://https://','https://'))
            with open('./CheckDate/task3CK/' + str(year) + '.txt', 'a+') as fcheck:
                fcheck.write(file+'\n')
    with open('./CheckDate/task3CK/yearcheck.txt', 'a+') as ycheck:
        ycheck.write(str(year)+'\n')


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
    try:
        WebDriverWait(browser, 30, 3).until(lambda browser:browser.find_element_by_xpath('//div[@class="PCD_counter"]/div[@class="WB_innerwrap"]/table[@class="tb_counter"]/tbody/tr/td/a[@class="t_link S_txt1"]'))
    except:
        try:
            infoBtn = browser.find_element_by_xpath("//a[contains(@href,'info?mod=pedit_more')]/span")
        except:
            infoBtn = browser.find_element_by_xpath("//a[contains(@href,'about')]/span")
        infoBtn.click()
        try:
            browser.refresh()
            WebDriverWait(browser, 30, 3).until(lambda browser: browser.find_element_by_xpath("//a[contains(@href,'follow?from=page')]"))
        except:
            print '??'
        browser.back()
        try:
            browser.refresh()
            WebDriverWait(browser, 30, 3).until(lambda browser:browser.find_element_by_xpath('//div[@class="PCD_counter"]/div[@class="WB_innerwrap"]/table[@class="tb_counter"]/tbody/tr/td/a[@class="t_link S_txt1"]'))
        except:
            print '???'
    try:
        allckick = browser.find_element_by_link_text(u'全部')
    except:
        try:
            allckick = browser.find_element_by_link_text('全部')
            allckick.click()
        except:
            try:
                browser.refresh()
                WebDriverWait(browser, 30, 3).until(lambda browser: browser.find_element_by_xpath('//a[@suda-data="key=tblog_profile_new&value=weibo_all"]'))
                allckick = browser.find_element_by_link_text('全部')
                allckick.click()
            except:
                try:
                    allckick = browser.find_element_by_xpath('//a[@suda-data="key=tblog_profile_new&value=weibo_all"]')
                    allckick.click()
                except:
                    url_all = url+'?profile_ftype=1&is_all=1#_0'
                    browser.get(url_all)

    try:
        browser.refresh()
        WebDriverWait(browser, 30, 3).until(lambda browser:browser.find_element_by_xpath('//div[@class="PCD_counter"]/div[@class="WB_innerwrap"]/table[@class="tb_counter"]/tbody/tr/td/a[@class="t_link S_txt1"]'))
    except:
        print '????'
    print "进入主页..."

    time.sleep(random.random()+10*random.random())
    homepage = browser.page_source
    homeurl = browser.current_url
    try:
        Wuser["follow_num"] = browser.find_element_by_xpath("//a[contains(@href,'follow?from=page')]/strong").text
        Wuser["fans_num"] = browser.find_element_by_xpath("//a[contains(@href,'follow?relate=fans')]/strong").text
        Wuser["weibo_num"] = browser.find_element_by_xpath("//a[contains(@href,'home?from=page')]/strong").text
    except:
        send_mail.mail()
        print '有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒有毒'
        Wuser["follow_num"] = 'none'
        Wuser["fans_num"] = 'none'
        Wuser["weibo_num"] = 'none'
    if(id.isdigit()):
        Wuser["is_bigV"] = 'N'
    else:
        Wuser["is_bigV"] = 'Y'
    Wuser["repo_num"] = 0
    Wuser["comment_num"] = 0
    Wuser["like_num"] = 0
    repos = browser.find_elements_by_xpath("//span[@node-type='forward_btn_text']/span/em[2]")
    for r in repos:
        print 'r:',r
        if(r.text.isdigit()):
            Wuser["repo_num"] = Wuser["repo_num"]+int(r.text)
        else:
            Wuser["repo_num"] = Wuser["repo_num"]+0

    comments = browser.find_elements_by_xpath("//span[@node-type='comment_btn_text']/span/em[2]")
    for c in comments:
        print 'c:',c
        if(c.text.isdigit()):
            Wuser["comment_num"] = Wuser["comment_num"]+int(c.text)
        else:
            Wuser["comment_num"] = Wuser["comment_num"]+0

    like = browser.find_elements_by_xpath("//span[@node-type='like_status']/span/em[2]")
    for l in like:
        print "l:",l
        if(l.text.isdigit()):
            Wuser["like_num"] = Wuser["like_num"]+int(l.text)
        else:
            Wuser["like_num"] = Wuser["like_num"]+0
    print "主页获取完毕..."
    try:
        infoBtn = browser.find_element_by_xpath("//a[contains(@href,'info?mod=pedit_more')]/span")
    except:
        infoBtn = browser.find_element_by_xpath("//a[contains(@href,'about')]/span")
    infoBtn.click()
    try:
        browser.refresh()
        WebDriverWait(browser, 30, 3).until(lambda browser:browser.find_element_by_xpath("//a[contains(@href,'follow?from=page')]"))
    except:
        print '?????'
    print "进入资料页..."
    time.sleep(random.random()+10*random.random())
    infopage = browser.page_source
    infourl = browser.current_url
    print "资料页获取完毕..."
    try:
        followBtn = browser.find_element_by_xpath("//a[contains(@href,'follow?from=page')]")
        followBtn.click()
    except:
        browser.get(infourl.replace('about','follow'))
    try:
        browser.refresh()
        WebDriverWait(browser, 30, 3).until(lambda browser:browser.find_element_by_xpath('//div[@class="WB_frame"]/div[@id="plc_main"]'))
    except:
        print "??????"
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
    print Wuser
    with open("./weibo_user/"+str(id)+".json",'w') as hh:
        oo = json.dumps(Wuser,ensure_ascii=False)
        hh.write(oo)
        print id,"写入完毕"
    if(Downloadpage != '-1'):
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



def star(choose = '-1'):
    Downloadpage = choose
    init_spider()
    load_req()

if __name__ == '__main__':
    try:
        star()
    except Exception,error:
        times = 0
        rangetime = 10
        while ('Connection refused' in erro or 'Timeout' in erro or 'Timeout loading page after 300000ms' in erro):
            browser.quit()
            times = times + 1
            if (times > 3):
                rangetime = 30
            if (time > 4):
                send_mail.mail(Title='task3出现问题', message='mmp,我睡了一个小时，试了4次都失败了，你来搞一下吧')
                sys.exit()
            print "我睡" + str(rangetime) + "分钟"
            for i in range(0, rangetime):
                time.sleep(60)
                print "还有" + str(rangetime - i) + "分钟"
            try:
                erro = star()
            finally:
                print 'again'
