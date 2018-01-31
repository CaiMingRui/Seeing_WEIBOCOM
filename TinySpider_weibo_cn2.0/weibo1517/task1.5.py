# -*- coding:utf-8 -*-
from __future__ import division
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from xml.dom import minidom
import xml.dom.minidom
import re
import login
import datetime
import send_mail
import chardet
import os
import random
import urllib
import time
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")

browser = webdriver.Firefox(executable_path='./geckodriver',firefox_binary='/usr/lib/firefox57/firefox')
# 咦？暂时没有内容哦，稍后再来试试吧~~
def get_web(path):
    if(os.path.exists(path)):
        with open(path,'r') as r:
            list = r.read()
    else:
        print "没有这个文件夹"
    name=re.findall("<movie_name>:(.*?)</movie_name>",list)
    count = 1

    for i in name:
        url=re.findall("<"+i+"_url>:(.*?)</"+i+"_url>",list)
        if(os.path.exists('./CheckDate/getwebdatecheck/checkurl.txt')):
            with open('./CheckDate/getwebdatecheck/checkurl.txt', 'r') as xx:
                xxl = xx.readlines()
            if url[0]+'\n' in xxl:
                print url[0],'pass'
                continue
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        print "star_"+str(count)+"_"+i
        url=re.findall("<"+i+"_url>:(.*?)</"+i+"_url>",list)
        year=re.findall("<"+i+"_year>:(.*?)</"+i+"_year>",list)
        wid = re.findall("<"+i+"_wid>:(.*?)</"+i+"_wid>",list)
        time.sleep(1)
        count=count+1
        get_user(i,url[0],year[0],wid[0])
        with open('./CheckDate/getwebdatecheck/checkurl.txt','a') as yy:
            yy.writelines(url[0]+'\n')

def get_user(name,url,year,wid):#获取了评论用户的url和评论，保存在对应年份的电影文档里面了
    time.sleep(5*random.random())
    print "star get_user("+name+","+url+","+str(year)+")"
    browser.get(url)
    browser.refresh()
    WebDriverWait(browser, 30, 3).until(lambda browser: browser.find_element_by_xpath('//a[@class="WB_cardmore WB_cardmore_noborder S_txt1 clearfix"]/span[@class="more_txt"]'))
    browser.execute_script("window.scrollTo(100000,document.body.scrollHeight);")
    time.sleep(10*random.random())
    moretext = url+'/review?feed_filter=1'
    browser.get(moretext)
    WebDriverWait(browser, 30, 3).until(lambda browser: browser.find_element_by_xpath('//div[@class="tab_box tab_box_b tab_box_b_r2 clearfix"]/ul[@class="tab W_fl clearfix"]/li[@class="curr"]'))

    for i in range(1, 3):# at most 2 times
        browser.execute_script("window.scrollTo(100000,document.body.scrollHeight);")
        time.sleep(3)
        try:
            # 定位页面底部的换页tab
            browser.find_element_by_xpath('//span[@class="list"]/a[@action-type="feed_list_page_more"]')
            break  # 如果没抛出异常就说明找到了底部标志，跳出循环
        except:
            pass  # 抛出异常说明没找到底部标志，继续向下滑动
    browser.execute_script("window.scrollTo(100000,document.body.scrollHeight);")

    print browser.current_url

    try:
        comment_more_url = []
        user_id = browser.find_elements_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@class="WB_cardwrap WB_feed_type S_bg2 WB_feed_like"]')
        protecnumA = 0
        for iu in user_id:
            print "***********************************************************************************************************"
            id = iu.get_attribute('tbinfo')
            comment_id = browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]').get_attribute('mid')
            if (os.path.exists('./user_url_comments/' + str(year) + '/' + name + ".json")):
                print "ossssssssssssssssssssssssss"
                with open('./user_url_comments/' + str(year) + '/' + name + ".json", 'r') as ch:
                    finish = ch.read()
                    finishid = re.findall('\[comment_id\]\:(.*?)\[/comment_id\]', finish)
                    if comment_id in finishid:
                        protecnumA = protecnumA+1
                        print "pass"
                        if(protecnumA>=80):
                            browser.refresh()
                            break
                        continue
            user_name=browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_info"]/a[@class="W_f14 W_fb S_txt1"]').get_attribute('nick-name')

            print "正在处理" + user_name

            user_url_un=browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="'+id+'"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_info"]/a[@class="W_f14 W_fb S_txt1"]').get_attribute('href')
            user_url = user_url_un.replace('http://https://','https://')
            ctime = browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a').text
            try:
                star = browser.find_elements_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"]/img[@title="[星星]"]')

            except:
                print "没有星星×××"

            try:
                halfstar = browser.find_elements_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"]/img[@title="[半星]"]')
            except:
                print "没有半星"


            cstar = 0
            hstar = 0
            for i in star:
                cstar = cstar+1
            for j in halfstar:
                hstar = hstar+1

            score = 2*cstar+hstar

            pathF = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li[2]/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="转发"]'
            if(more_C(pathF)):
                forward = browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li[2]/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[2]').text
            else:
                forward = 0

            pathL = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li[4]/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="赞"]'
            if(more_C(pathL)):
                like_num = browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li[4]/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[2]').text
            else:
                like_num = 0

            pathX = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="评论"]'
            if(more_C(pathX)):
                print user_name+"有评论"
                mreClick = browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]//span[@node-type="comment_btn_text"]')
                mreClick.click()
                time.sleep(5)
                pathY = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_repeat S_bg1"]/div[@class="WB_feed_repeat S_bg1 WB_feed_repeat_v3"]//div[@class="repeat_list"]/div[@class="list_box"]/div[@class="list_ul"]/a'
                if (is_exist(pathY)):
                    url =  browser.find_element_by_xpath(pathY).get_attribute('href')
                    print user_name+"有更多评价链接"
                    comment_more_url.append(url)


            pathA = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"]'
            pathB = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"and@node-type="feed_list_content_full"]'
            pathC = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"]/a[@class="WB_text_opt"]'


            if (is_exist(pathC)):
                TextBtn = browser.find_element_by_xpath(pathC)
                TextBtn.click()
                print user_name+" is open for text"
                time.sleep(3)
                user_txt = browser.find_element_by_xpath(pathB).text
            else:
                user_txt = browser.find_element_by_xpath(pathA).text
                print user_name+" no open for text"

            if(score == 0):
                if '★' in user_txt:
                    print user_txt
                    print "wow!!评论里面有❤❤诶！！！"
                    xinxinnum = 0
                    xinxin = re.findall(u'(★)',user_txt)
                    for i in xinxin:
                        print i
                        xinxinnum=xinxinnum+1
                    score = 2*xinxinnum
                    print "score:",score

            if(os.path.exists('./user_url_comments/'+str(year))==False):
                os.mkdir('./user_url_comments/'+str(year))
            with open('./user_url_comments/'+str(year)+'/'+name+".json",'a') as r:
                r.write(
                    "------------------------------------------------------------------------------------\n"
                    + "[wid]:" + wid + "[/wid]"+'\n'
                    +"[user_name]:"+user_name+"[/user_name]"+'\n'
                    +"[user_url]:"+user_url+"[/user_url]"+'\n'
                    +"[comment_id]:"+str(comment_id)+"[/comment_id]"+'\n'
                    +"[ctime]:"+ctime+"[/ctime]"+'\n'
                    +"[score]:"+str(score)+"[/score]"+'\n'
                    +"[forward]:"+str(forward)+"[/forward]"+'\n'
                    +"[like_num]:"+str(like_num)+"[/like_num]"+'\n'
                    +"[user_txt]:"+user_txt+"[/user_txt]"+'\n'
                    +"-----------------------------------------------------------------------------------"
                )



        while(check_nextpage()):
            time.sleep(3)
            ClickBtn = browser.find_element_by_link_text("下一页")
            ClickBtn.click()
            WebDriverWait(browser, 30, 3).until(lambda browser: browser.find_element_by_xpath(
                '//div[@class="tab_box tab_box_b tab_box_b_r2 clearfix"]/ul[@class="tab W_fl clearfix"]/li[@class="curr"]'))
            protecnumB = 0
            for i in range(1, 3):  # at most 3 times
                browser.execute_script("window.scrollTo(100000,document.body.scrollHeight);")
                time.sleep(3)
                try:
                    # 定位页面底部的换页tab
                    browser.find_element_by_xpath('//span[@class="list"]/a[@action-type="feed_list_page_more"]')
                    break  # 如果没抛出异常就说明找到了底部标志，跳出循环
                except:
                    pass  # 抛出异常说明没找到底部标志，继续向下滑动
            browser.execute_script("window.scrollTo(100000,document.body.scrollHeight);")

            print browser.current_url
            user_id = browser.find_elements_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@class="WB_cardwrap WB_feed_type S_bg2 WB_feed_like"]')
            for iu in user_id:
                print "***********************************************************************************************************"
                id = iu.get_attribute('tbinfo')
                comment_id = browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]').get_attribute('mid')
                if (os.path.exists('./user_url_comments/' + str(year) + '/' + name + ".json")):
                    print "osssssssssssssssssssssssssssssssssssssss"
                    with open('./user_url_comments/' + str(year) + '/' + name + ".json", 'r') as ch:
                        finish = ch.read()
                        finishid = re.findall('\[comment_id\]\:(.*?)\[/comment_id\]', finish)
                        if comment_id in finishid:
                            protecnumB=protecnumB+1
                            print "pass"
                            if(protecnumB>=80):
                                browser.refresh()
                                break
                            continue
                user_name = browser.find_element_by_xpath(
                    '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_info"]/a[@class="W_f14 W_fb S_txt1"]').get_attribute('nick-name')
                user_url = "http://" + browser.find_element_by_xpath(
                    '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_info"]/a[@class="W_f14 W_fb S_txt1"]').get_attribute('href')
                print "正在处理" + user_name

                ctime = browser.find_element_by_xpath(
                    '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a').text
                try:
                    star = browser.find_elements_by_xpath(
                        '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"]/img[@title="[星星]"]')

                except:
                    print "没有星星×××"

                try:
                    halfstar = browser.find_elements_by_xpath(
                        '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"]/img[@title="[半星]"]')
                except:
                    print "没有半星"

                cstar = 0
                hstar = 0
                for i in star:
                    cstar = cstar + 1
                for j in halfstar:
                    hstar = hstar + 1

                score = 2 * cstar + hstar

                pathF = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li[2]/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="转发"]'
                if (more_C(pathF)):
                    forward = browser.find_element_by_xpath(
                        '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li[2]/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[2]').text
                else:
                    forward = 0

                pathL = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li[4]/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="赞"]'
                if (more_C(pathL)):
                    like_num = browser.find_element_by_xpath(
                        '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li[4]/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[2]').text
                else:
                    like_num = 0

                pathX = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li[3]/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="评论"]'
                if (more_C(pathX)):
                    print user_name + "有评论"
                    mreClick = browser.find_element_by_xpath(
                        '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]//span[@node-type="comment_btn_text"]')
                    mreClick.click()
                    time.sleep(5)
                    pathY = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_repeat S_bg1"]/div[@class="WB_feed_repeat S_bg1 WB_feed_repeat_v3"]//div[@class="repeat_list"]/div[@class="list_box"]/div[@class="list_ul"]/a'

                    if(is_exist(pathY)):
                        url = browser.find_element_by_xpath(pathY).get_attribute('href')
                        print user_name + "有更多评价链接"
                        comment_more_url.append(url)



                pathA = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"]'
                pathB = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"and@node-type="feed_list_content_full"]'
                pathC = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_text W_f14"]/a[@class="WB_text_opt"]'

                if (is_exist(pathC)):
                    TextBtn = browser.find_element_by_xpath(pathC)
                    TextBtn.click()
                    time.sleep(3)
                    user_txt = browser.find_element_by_xpath(pathB).text
                    print user_name + " is open for text"
                else:
                    user_txt = browser.find_element_by_xpath(pathA).text
                    print user_name + " no open for text"

                if (score == 0):
                    if '★' in user_txt:
                        print user_txt
                        print "wow!!评论里面有❤❤诶！！！"
                        xinxinnum = 0
                        xinxin = re.findall(u'(★)', user_txt)
                        for i in xinxin:
                            print i
                            xinxinnum = xinxinnum + 1
                        score = 2 * xinxinnum
                        print "score:", score

                if (os.path.exists('./user_url_comments/' + str(year)) == False):
                    os.mkdir('./user_url_comments/' + str(year))
                with open('./user_url_comments/' + str(year) + '/' + name + ".json", 'a') as r:
                    r.write(
                        "------------------------------------------------------------------------------------\n"
                        + "[wid]:" + str(wid) + "[/wid]" + '\n'
                        + "[user_name]:" + user_name + "[/user_name]" + '\n'
                        + "[user_url]:" + user_url + "[/user_url]" + '\n'
                        + "[comment_id]:" + str(comment_id) + "[/comment_id]" + '\n'
                        + "[ctime]:" + ctime + "[/ctime]" + '\n'
                        + "[score]:" + str(score) + "[/score]" + '\n'
                        + "[forward]:" + str(forward) + "[/forward]" + '\n'
                        + "[like_num]:" + str(like_num) + "[/like_num]" + '\n'
                        + "[user_txt]:" + user_txt + "[/user_txt]" + '\n'
                        + "-----------------------------------------------------------------------------------"
                    )

        if (os.path.exists("./more_comment_url/" + str(year)) == False):
            os.mkdir("./more_comment_url/" + str(year))

        with open("./more_comment_url/" + str(year) + "/" + name + ".json", 'a+') as w:
            for more_comment_url in comment_more_url:
                if more_comment_url+'\n' in w.readlines():
                    continue
                else:
                    w.write(more_comment_url + '\n')
        # return 'GOOD'
    # except Exception,e:
    #     print Exception,":",e
    #     return e

    finally:

        if (os.path.exists("./more_comment_url/" + str(year)) == False):
            os.mkdir("./more_comment_url/" + str(year))

        with open("./more_comment_url/" + str(year) + "/" + name + ".json", 'a') as w:
            for more_comment_url in comment_more_url:
                w.write(more_comment_url + '\n')
                print more_comment_url



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
    login.login(browser)
    # try:
    files = os.listdir('./movie_search_url/')
    for file in files:
        if os.path.exists('./CheckDate/getwebdate.txt'):
            with open('./CheckDate/getwebdate.txt', 'r') as rei:
                sabi = rei.readlines()
                if file in sabi:
                    continue
        path = './movie_search_url/' + file
        get_web(path)
        with open('./CheckDate/getwebdate.txt', 'w') as wri:
            wri.write(file + '\n')
    except  Exception, iio:
        print Exception,":",iio
        return iio


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
                send_mail.mail(Title='task1-5出现问题',message='mmp,我睡了一个小时，试了4次都失败了，你来搞一下吧')
                sys.exit()
            print "我睡"+str(rangetime)+"分钟"
            for i in range(0, rangetime):
                time.sleep(60)
                print "还有" + str(rangetime - i) + "分钟"
            try:
                erro = star()
            finally:
                print 'again'
                # send_mail.mail(Title='task1-5出现问题', message='未知错误，错误内容为：'+str(erro))
    except Exception,erro:
        print Exception,"xiaxiaxia:xiaxiaxia",erro
        send_mail.mail(Title='task1-5出现问题', message='未知错误，错误内容为：' + str(erro))

