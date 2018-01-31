# -*- coding:utf-8 -*-
from __future__ import division
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import smtplib
from email.mime.text import MIMEText
from selenium.webdriver.common.action_chains import ActionChains
from xml.dom import minidom
import xml.dom.minidom
import re
import login
import send_mail
import datetime
import chardet
import os
import random
import urllib
import time
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
#task1 作为整个爬虫任务的第一部分，主要完成了获取电影的目标网址，获取了电影的评论，同时保存了电影的评论用户的链接
#task2 作为第二部分，主要是将扩充评论里的评论用户的链接获取下来，存到task3要用的用户url列表中
#task3 作为任务的第二部分，主要是通过task1获得的用户链接，去获取用户的三个主界面。



######################
#                    #
#       task1        #
#                    #
######################


browser = webdriver.Firefox()
dict = {}

def init_spider():
    login.login(browser)
    return browser

def load_req(json_array_movie):
    print "-----------------star to search"+json_array_movie["Movie_name"]+"-------------------------"
    # print urllib.quote(json_array_movie["Movie_name"])
    browser.get("http://s.weibo.com/weibo/"+urllib.quote(json_array_movie["Movie_name"])+"&Refer=p")
    try:
        time.sleep(3)
        print browser.current_url
        # browser.find_element_by_id('plc_main')
        browser.find_element_by_class_name('code_ver')
        # browser.find_element_by_partial_link_text(u"行为有些异常")
        # browser.find_element_by_partial_link_text(u"验证码")
        print '找到验证码'
        ret = send_mail.mail(Title='task1验证码',message='boss!task1有验证码啦！！！回来看看啊！')
        if ret:
            print("已发送提醒")
        else:
            time.sleep(60)
            print("提醒失败,重试一次")
            send_mail.mail(Title='task1验证码',message='boss!task1有验证码啦！！！回来看看啊！')
        while True:
            flag = raw_input('继续请输入Y，否则按任意键')
            if flag.upper() == 'Y':
                for i in range(0,4):
                    time.sleep(1)
                    print str(4-i)+"秒后重新获取界面"
                browser.get("http://s.weibo.com/weibo/" + urllib.quote(json_array_movie["Movie_name"]) + "&Refer=p")
                break
    except:
        print '安全通过'
    try:
        browser.find_element_by_class_name('search_noresult')
        print "未找到“" + json_array_movie["Movie_name"] + "”相关结果。 "
        return
    except:
        try:
            browser.find_element_by_xpath('//div[@id="pl_weibo_directtop"]/div[@class="WB_cardwrap S_bg2 wbs_interest_dir"]/div[@class="interest_content"]/div[@class="film_content"]/div[@class="detail"]/h1/a[@class="name"]')
            getname = browser.find_element_by_xpath('//div[@id="pl_weibo_directtop"]/div[@class="WB_cardwrap S_bg2 wbs_interest_dir"]/div[@class="interest_content"]/div[@class="film_content"]/div[@class="detail"]/h1/a[@class="name"]').text
            if(getname == json_array_movie["Movie_name"]):
                print "找到" + json_array_movie["Movie_name"]
        except:
            print "未找到“" + json_array_movie["Movie_name"] + "”相关结果。 "
            return

    # clickBtn = browser.find_elements_by_xpath('//div[@class="film_content"]/div[@class="pic"]')[0]#这里可能会有问题，可能需要更加明确以下,例如在后面加个[0]
    clickBtn = browser.find_element_by_xpath('//div[@id="pl_weibo_directtop"]/div[@class="WB_cardwrap S_bg2 wbs_interest_dir"]/div[@class="interest_content"]/div[@class="film_content"]/div[@class="detail"]/h1/a[@class="name"]')
    clickBtn.click()
    handow = browser.current_window_handle
    browser.switch_to.window(browser.window_handles[-1])
    browser.switch_to.window(browser.window_handles[-1])
    browser.switch_to.window(browser.window_handles[-1])

    time.sleep(5)
    print browser.current_url
    for i in range(0,5):
        browser.switch_to.window(browser.window_handles[-1])
        browser.switch_to.window(browser.window_handles[-1])
        browser.switch_to.window(browser.window_handles[-1])
        time.sleep(1)
        print "还有"+str(5-i)+"秒"
        print browser.current_url
    WebDriverWait(browser, 30, 3).until(lambda browser: browser.find_element_by_xpath('//div[@class="send_weibo send_weibo_simple clearfix send_weibo_long"]/div[@class="WB_innerwrap"]'))
    url=browser.current_url
    wid = re.sub("https://weibo\.com/p/","",url)
    try:
        browser.find_element_by_xpath('//div[@class="pf_username clearfix"]/span[@class="remark"]/span[@class="remark_score W_Yahei"]')
        rating = browser.find_element_by_xpath('//div[@class="pf_username clearfix"]/span[@class="remark"]/span[@class="remark_score W_Yahei"]').text
    except:
        print "没有电影评分"
        rating = 'none'
    # Rating_num = browser.find_element_by_xpath("//span[@text()='打分']/../strong").text
    try:
        browser.find_element_by_xpath('//div[@class="WB_innerwrap"]/table[@class="tb_counter"]/tbody/tr/td[2]/strong')
        print browser.find_element_by_xpath('//div[@class="WB_innerwrap"]/table[@class="tb_counter"]/tbody/tr/td[2]/span').text
        Rating_num = browser.find_element_by_xpath('//div[@class="WB_innerwrap"]/table[@class="tb_counter"]/tbody/tr/td[2]/strong').text
        if(Rating_num == '-'):
            Rating_num = 'none'
    except:
        print "没人打分"
        Rating_num = 'none'
    try:
        browser.find_element_by_xpath('//div[@class="WB_innerwrap"]/table[@class="tb_counter"]/tbody/tr/td[1]/strong')
        print browser.find_element_by_xpath('//div[@class="WB_innerwrap"]/table[@class="tb_counter"]/tbody/tr/td[1]/span').text
        Follow_num = browser.find_element_by_xpath('//div[@class="WB_innerwrap"]/table[@class="tb_counter"]/tbody/tr/td[1]/strong').text
        if(Follow_num == '-'):
            Follow_num = 'none'
    except:
        print "没有关注项"
        Follow_num = 'none'
    Story = browser.find_element_by_class_name('p_txt').text
    print json_array_movie["Movie_name"]+" 的主页链接为:"+url
    time.sleep(3)

    with open("./movie_search_url/" + str(json_array_movie["year"]) + ".txt", 'a') as w:

        w.write("<movie_name>:" + json_array_movie["Movie_name"] + "</movie_name>\n")
        w.write("<" + json_array_movie["Movie_name"] + "_year>:" + str(json_array_movie["year"]) + "</" + json_array_movie["Movie_name"] + "_year>\n")
        w.write("<" + json_array_movie["Movie_name"] + "_url>:" + url + "</" + json_array_movie["Movie_name"] + "_url>\n")
        w.write("<" + json_array_movie["Movie_name"] + "_wid>:" + str(wid) + "</" + json_array_movie["Movie_name"] + "_wid>\n")
        w.write("<" + json_array_movie["Movie_name"] + "_rating>:" + str(rating) + "</" + json_array_movie["Movie_name"] + "_rating>\n")
        w.write("<" + json_array_movie["Movie_name"] + "_Rating_num>:" + str(Rating_num) + "</" + json_array_movie["Movie_name"] + "_Rating_num>\n")
        w.write("<" + json_array_movie["Movie_name"] + "_Follow_num>:" + str(Follow_num) + "</" + json_array_movie["Movie_name"] + "_Follow_num>\n")
        w.write("<" + json_array_movie["Movie_name"] + "_Story>:" + Story + "</" + json_array_movie["Movie_name"] + "_Story>\n")
        w.write("-------------------------------------------------------------------\n")
    browser.close()
    browser.switch_to.window(handow)

def is_exist(path):
    try:
        browser.find_element_by_xpath(path)
        return True
    except:
        return False

def check_nextpage():
    try:
        browser.find_element_by_link_text("下一页")
        print "found next PAGE"
        return True
    except:
        print "This is the last page"
        return False

def more_C(pathX):
    try:
        browser.find_element_by_xpath(pathX)
        return False
    except:
        return True


def star():
    try:
        init_spider()
        json_array_movie = {}
        list = os.listdir('./movie_time_name/')
        for i in list:
            if (os.path.exists('./CheckDate/year.txt')):
                with open('./CheckDate/year.txt', 'r') as r:
                    yy = r.readlines()
                    if i.replace('.txt', '')+'\n' in yy:
                        print i + "已完成"
                        continue
            qq = codecs.open('./movie_time_name/' + i, 'r')
            # with open('./movie_time_name/'+i,'r') as r:
            print "open " + i
            text = qq.readlines()
            print text
            for j in text:
                if (os.path.exists('./CheckDate/' + i)):
                    with open('./CheckDate/' + i, 'r') as ee:
                        ii = ee.readlines()
                        if j in ii:
                            print j + "已完成"
                            continue
                year = i.replace('.txt', '')
                print "star ", year, j
                name = j
                # nameq = urllib.quote(name)
                # print nameq
                json_array_movie["Movie_name"] = name.replace('\n', '')
                json_array_movie["year"] = year
                load_req(json_array_movie)
                with open('./CheckDate/' + i, 'a') as checky:
                    checky.write(j)
            with open('./CheckDate/year.txt', 'a') as checkn:
                checkn.write(i.replace('.txt', '')+'\n')
        return 'GOOD'
    except Exception, x:
        print Exception, ":", x
        return x



if __name__ == '__main__':
    try:
        erro = star()
        times = 0
        rangetime = 10
        while ('Connection refused' in erro or 'Timeout' in erro or 'Timeout loading page after 300000ms' in erro):
            browser.quit()
            times = times + 1
            if(times>3):
                rangetime = 30
            if(time>4):
                send_mail.mail(Title='task1出现问题',message='mmp,我睡了一个小时，试了4次都失败了，你来搞一下吧')
                sys.exit()
            print "我睡"+str(rangetime)+"分钟"
            for i in range(0, rangetime):
                time.sleep(60)
                print "还有" + str(rangetime - i) + "分钟"
            try:
                erro = star()
            finally:
                print 'again'
                # print Exception,':vvvvv',erro
                # send_mail.mail(Title='task1出现问题', message='未知错误，错误内容为：'+str(erro))
    except Exception,E:
        print Exception,":",E
        send_mail.mail(Title='task1出现问题', message='未知错误，错误内容为：' + str(E))
