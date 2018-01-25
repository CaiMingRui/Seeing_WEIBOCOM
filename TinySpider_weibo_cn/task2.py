# -*- coding:utf-8 -*-
from __future__ import division
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from xml.dom import minidom
import xml.dom.minidom
import re
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
#       task2        #
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
    years = os.listdir("./more_comment_url/")
    for year in years:
        names = os.listdir("./more_comment_url/"+str(year)+"/")
        for i in names:
            name = i.replace(".json","")
            with open("./more_comment_url/" + str(year) + "/" + i, "r") as r:
                urls = r.readlines()
                for url in urls:
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~新的评论页啦！！~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    print year,name,url

                    url.replace('/n','')
                    exec_spider(year,name,url)


def exec_spider(year,name,url):
    browser.get(url)
    WebDriverWait(browser, 30, 3).until(lambda browser: browser.find_element_by_xpath('//div[@class="WB_feed_repeat S_bg1 WB_feed_repeat_v3"]'))
    time.sleep(4)
    browser.execute_script("window.scrollTo(100000,document.body.scrollHeight);")
    time.sleep(10)
    num = 0
    # path = '//a[@class="WB_cardmore WB_cardmore_v2 S_txt1 S_line1 clearfix"]/span[@class="more_txt"]'

    while(num<=50):
        print "\n正在加载更多内容...\n","第"+str(num)+"次"
        browser.execute_script("window.scrollTo(100000,document.body.scrollHeight);")
        time.sleep(7)
        # if(num < 5):
        #
        #     if(check_child()):
        #         clickBtn = browser.find_elements_by_partial_link_text("条回复")
        #         for i in clickBtn:
        #             i.click()
        #             time.sleep(10*random.random())
        if(check_more()):
            more_txtBtn =browser.find_element_by_xpath('//a[@suda-uatrack="key=click comments&value=click:singl_weibo:1"]')
            print "Click 查看更多！！",num
            more_txtBtn.click()
            print "I am sleeping!!!!"
            time.sleep(random.randint(4,10))
            print "Good morning!!!!!"
            num=num+1
        else:
            print "没有更多评价啦！！"
            break

    print "×××××××××××××××××××××××××××展开结束，开始爬用户××××××××××××××××××××××××××××××××"

    count = 0
    ids = browser.find_elements_by_xpath('//div[@class="list_ul"]/div[@class="list_li S_line1 clearfix"]')

    print ids

    for i in ids:
        count = count+1
        print "第"+str(count)+"个"
        comment_id = i.get_attribute("comment_id")
        user = browser.find_element_by_xpath('//div[@class="list_li S_line1 clearfix"and@comment_id="'+str(comment_id)+'"]/div[@class="list_con"]/div[@class="WB_text"]/a[@usercard]').get_attribute("usercard")
        user_name = browser.find_element_by_xpath('//div[@class="list_li S_line1 clearfix"and@comment_id="'+str(comment_id)+'"]/div[@class="list_con"]/div[@class="WB_text"]/a[@usercard]').text
        user_url = "https://weibo.com/u/"+str(user.replace("id=",""))
        user_txt = browser.find_element_by_xpath('//div[@class="list_li S_line1 clearfix"and@comment_id="'+str(comment_id)+'"]/div[@class="list_con"]/div[@class="WB_text"]').text
        print user_name,comment_id,user_url
        if (os.path.exists('./more_user_url_comments/' + str(year)) == False):
            os.mkdir('./more_user_url_comments/' + str(year))
        with open('./more_user_url_comments/' + str(year) + '/' + name + ".json", 'a') as r:
            r.write(
                "------------------------------------------------------------------------------------\n"
                + "[user_name]:" + user_name + "[/user_name]" + '\n'
                + "[user_url]:" + user_url + "[/user_url]" + '\n'
                + "[user_txt]:" + user_txt + "[/user_txt]" + '\n'
                + "-----------------------------------------------------------------------------------\n"
            )

        # path = '//div[@class="list_ul"]/div[@class="list_li S_line1 clearfix"and@comment_id="'+str(comment_id)+'"]/div[@class="list_con"]/div[@class="list_box_in S_bg3"]'
        # if(find_res(path,user_name)):
        #     print "---------------------正在获取儿子-------------------------------------"
        #     print "---------------------正在获取儿子-------------------------------------"
        #     print "---------------------正在获取儿子-------------------------------------"
        #     print "---------------------正在获取儿子-------------------------------------"
        #     print "---------------------正在获取儿子-------------------------------------"
        #     child = browser.find_elements_by_xpath('//div[@class="list_ul"]/div[@comment_id="'+str(comment_id)+'"]/div[@class="list_con"]/div[@class="list_box_in S_bg3"]/div[@node-type="child_comment"]/div[@comment_id]')
        #     print child
        #     for c in child:
        #         child_id = c.get_attribute("comment_id")
        #         child_name = browser.find_element_by_xpath('//div[@class="list_li S_line1 clearfix"and@comment_id="'+str(comment_id)+'"]/div[@class="list_con"]/div[@class="list_box_in S_bg3"]/div[@node-type="child_comment"]/div[@class="list_li S_line1 clearfix"and@comment_id="'+str(child_id)+'"]/div[@class="list_con"]/div[@class="WB_text"]/a[@usercard]').text
        #         user_id = browser.find_element_by_xpath('//div[@class="list_li S_line1 clearfix"and@comment_id="'+str(comment_id)+'"]/div[@class="list_con"]/div[@class="list_box_in S_bg3"]/div[@node-type="child_comment"]/div[@class="list_li S_line1 clearfix"and@comment_id="'+str(child_id)+'"]/div[@class="list_con"]/div[@class="WB_text"]/a[@usercard]').get_attribute('usercard')
        #         child_url = "https://weibo.com/u/" + str(user_id.replace("id=",""))
        #
        #         print "\n儿子："+child_name,child_url
        #
        #         if (os.path.exists('./more_user_url_comments/' + str(year)) == False):
        #             os.mkdir('./more_user_url_comments/' + str(year))
        #         with open('./more_user_url_comments/' + str(year) + '/' + name + ".json", 'a') as r:
        #             r.write(
        #                 "------------------------------------------------------------------------------------\n"
        #                 + "[user_name]:" + child_name + "[/user_name]" + '\n'
        #                 + "[user_url]:" + child_url + "[/user_url]" + '\n'
        #                 + "[user_txt]:" + "NUN" + "[/user_txt]" + '\n'
        #                 + "-----------------------------------------------------------------------------------\n"
        #             )


def find_res(path,user_name):
    try:
        browser.find_element_by_xpath(path)
        print user_name+"找到回复啦！"
        return True
    except:
        print user_name+"没有回复哎！"


def check_child():
    try:
        browser.find_elements_by_partial_link_text("条回复")
        return True
    except:
        return False


def check_more():
    try:
        browser.find_element_by_xpath('//a[@suda-uatrack="key=click comments&value=click:singl_weibo:1"]')
        print "找到更多评论"
        return True
    except:

        return False



if __name__ == '__main__':
    init_spider()
    load_req()

