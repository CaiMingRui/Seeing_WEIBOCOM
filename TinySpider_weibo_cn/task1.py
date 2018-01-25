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
#       task1        #
#                    #
######################


browser = webdriver.Firefox()
dict = {}

# def init_spider(dict_args):
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
        userBtn.send_keys("userid")
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
        print '*******************************login(id) fail******************************'
        print Exception,":",r
        print '*******************************login(id) fail******************************'

# def login():
#     """
#     进行微博的手动登陆
#     :return: null
#     """
#     browser.get("http://weibo.com/")
#     while True:
#         flag = raw_input('继续请输入Y，否则按任意键')
#         if flag.upper() == 'Y':
#             break

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

def load_req(json_array_movie):
    print "-----------------------------star to search"+json_array_movie["Movie_name"]+"---------------------------------"
    browser.get("http://s.weibo.com/weibo/"+urllib.quote(json_array_movie["Movie_name"])+"&Refer=p")
    try:
        browser.find_element_by_class_name('search_noresult')
        print "找到"+json_array_movie["Movie_name"]
    except:
        print "未找到“"+json_array_movie["Movie_name"]+"”相关结果。 "
        return
    clickBtn = browser.find_elements_by_xpath('//div[@class="film_content"]/div[@class="pic"]')[0]#这里可能会有问题，可能需要更加明确以下,例如在后面加个[0]
    clickBtn.click()
    browser.switch_to.window(browser.window_handles[-1])
    WebDriverWait(browser, 30, 3).until(lambda browser: browser.find_element_by_xpath('//div[@class="PCD_piclist_a PCD_piclist_a3"]/div[@class="WB_cardtitle_b S_line2"]'))
    url=browser.current_url
    wid = re.sub("https://weibo\.com/p/","",url)
    rating = browser.find_element_by_class_name('remark_score W_Yahei').text
    Rating_num = browser.find_element_by_xpath("//span[@text()='打分']/preceding-sibling::strong").text
    Follow_num = browser.find_element_by_xpath("//span[@text()='关注']/preceding-sibling::strong").text
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

    path="./movie_search_url/" + str(json_array_movie["year"]) + ".txt"
    get_web(path)
    # 这句话只是在测试的时候用到的，在完整的代码中，这个函数的调用需要运用循环构建path文件，然后在分开调用get_web(path)


def get_web(path):
    if(os.path.exists(path)):
        with open(path,'r') as r:
            list = r.read()
    else:
        print "没有这个文件夹"
    name=re.findall("<movie_name>:(.*?)</movie_name>",list)
    count = 1
    for i in name:
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        print "star_"+str(count)+"_"+i
        url=re.findall("<"+i+"_url>:(.*?)</"+i+"_url>",list)
        year=re.findall("<"+i+"_year>:(.*?)</"+i+"_year>",list)
        wid = re.findall("<"+i+"_wid>:(.*?)</"+i+"_wid>",list)
        time.sleep(1)
        count=count+1
        get_user(i,url[0],year[0],wid)

def get_user(name,url,year,wid):#获取了评论用户的url和评论，保存在对应年份的电影文档里面了
    time.sleep(5*random.random())
    print "star get_user("+name+","+url+","+str(year)+")"
    browser.get(url)
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
    # js = 'var q=document.getElementsByClassName("WB_text W_f14");for(var i=0;i<q.length;i++){q[i].style.style=" ";}'
    # browser.execute_script(js)



    try:
        comment_more_url = []
        user_id = browser.find_elements_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@class="WB_cardwrap WB_feed_type S_bg2 WB_feed_like"]')
        for iu in user_id:
            print "***********************************************************************************************************"
            id = iu.get_attribute('tbinfo')
            user_name=browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_info"]/a[@class="W_f14 W_fb S_txt1"]').get_attribute('nick-name')

            print "正在处理" + user_name

            user_url=browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="'+id+'"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_info"]/a[@class="W_f14 W_fb S_txt1"]').get_attribute('href')
            comment_id = browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]').get_attribute('mid')
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

            pathF = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="转发"]'
            if(more_C(pathF)):
                forward = browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[2]').text
            else:
                forward = 0

            pathL = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="赞"]'
            if(more_C(pathL)):
                like_num = browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[2]').text
            else:
                like_num = 0

            pathX = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="评论"]'
            if(more_C(pathX)):
                print user_name+"有评论"
                mreClick = browser.find_element_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]//span[@node-type="comment_btn_text"]')
                mreClick.click()
                time.sleep(5)
                pathY = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_repeat S_bg1"]/div[@class="WB_feed_repeat S_bg1 WB_feed_repeat_v3"]/div[@class="WB_repeat S_line1"]/div[@class="repeat_list"]/div[@class="list_box"]/div[@class="list_ul"]/a[@class="WB_cardmore WB_cardmore_v2 S_txt1 S_line1 clearfix"]'
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


            if(os.path.exists('./user_url_comments/'+str(year))==False):
                os.mkdir('./user_url_comments/'+str(year))
            with open('./user_url_comments/'+str(year)+'/'+name+".json",'a') as r:
                r.write(
                    "------------------------------------------------------------------------------------\n"
                    + "[wid]:" + str(wid) + "[/wid]"+'\n'
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


            user_id = browser.find_elements_by_xpath('//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@class="WB_cardwrap WB_feed_type S_bg2 WB_feed_like"]')
            for iu in user_id:
                print "***********************************************************************************************************"
                id = iu.get_attribute('tbinfo')
                user_name = browser.find_element_by_xpath(
                    '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_info"]/a[@class="W_f14 W_fb S_txt1"]').get_attribute('nick-name')
                user_url = "http://" + browser.find_element_by_xpath(
                    '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_detail clearfix"]/div[@class="WB_detail"]/div[@class="WB_info"]/a[@class="W_f14 W_fb S_txt1"]').get_attribute('href')
                print "正在处理" + user_name

                comment_id = browser.find_element_by_xpath(
                    '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]').get_attribute('mid')
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

                pathF = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="转发"]'
                if (more_C(pathF)):
                    forward = browser.find_element_by_xpath(
                        '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[2]').text
                else:
                    forward = 0

                pathL = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="赞"]'
                if (more_C(pathL)):
                    like_num = browser.find_element_by_xpath(
                        '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[2]').text
                else:
                    like_num = 0

                pathX = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]/ul[@class="WB_row_line WB_row_r4 clearfix S_line2"]/li/a[@class="S_txt2"]/span[@class="pos"]/span/span/em[@text="评论"]'
                if (more_C(pathX)):
                    print user_name + "有评论"
                    mreClick = browser.find_element_by_xpath(
                        '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_handle"]/div[@class="WB_handle"]//span[@node-type="comment_btn_text"]')
                    mreClick.click()
                    time.sleep(5)
                    pathY = '//div[@class="WB_feed WB_feed_v3 WB_feed_v4"]/div[@tbinfo="' + id + '"]/div[@class="WB_feed_repeat S_bg1"]/div[@class="WB_feed_repeat S_bg1 WB_feed_repeat_v3"]/div[@class="WB_repeat S_line1"]/div[@class="repeat_list"]/div[@class="list_box"]/div[@class="list_ul"]/a[@class="WB_cardmore WB_cardmore_v2 S_txt1 S_line1 clearfix"]'
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

        with open("./more_comment_url/" + str(year) + "/" + name + ".json", 'a') as w:
            for more_comment_url in comment_more_url:
                w.write(more_comment_url + '\n')

    except Exception,e:
        print Exception,":",e

    finally:

        if (os.path.exists("./more_comment_url/" + str(year)) == False):
            os.mkdir("./more_comment_url/" + str(year))

        with open("./more_comment_url/" + str(year) + "/" + name + ".json", 'a') as w:
            for more_comment_url in comment_more_url:
                w.write(more_comment_url + '\n')
                print more_comment_url
        browser.quit()

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

if __name__ == '__main__':
    try:
        init_spider()
        json_array_movie = {}
        list = os.listdir('./movie_time_name')
        for i in list:
            if(os.path.exists('./CheckDate/year.txt')):
                with open('./CheckDate/year.txt','r') as r:
                    yy = r.read()
                    if i in r.read():
                        continue
            with open('./movie_time_name'+i,'r') as r:
                text = r.read()
                for j in text:
                    if(os.path.exists('./CheckDate/'+i)):
                        with open('./CheckDate/'+i,'r') as ee:
                            ii = ee.read()
                            if j in ii:
                                continue
                    year = i.replace('.txt','')
                    name = j
                    json_array_movie = {
                        "Movie_name": name,
                        "year": year
                    }
                    load_req(json_array_movie)
                    with open('./CheckDate/'+i,'a') as checky:
                        checky.write(j)
            with open('./CheckDate/year.txt','a') as checkn:
                checkn.write(i.replace('.txt',''))
    except Exception,x:
        print Exception,":",x
