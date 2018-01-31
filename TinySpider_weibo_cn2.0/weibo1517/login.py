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
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")



def login(browser,username = '13725774384',password = 'pachong'):
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
        userBtn.send_keys(username)
        time.sleep(2)
        # ActionChains.move_to_element(passBtn).click()
        passBtn.send_keys(password)
        time.sleep(1)
        Btn=browser.find_element_by_xpath("//div[@class='info_list login_btn']/a/span[@node-type='submitStates']")
        ActionChains(browser).move_to_element(Btn).perform()
        Btn.click()
        WebDriverWait(browser, 30, 3).until(lambda browser: browser.find_element_by_xpath('//div[@class="WB_innerwrap"]/div[@class="nameBox"]'))
        print "----------------------------have been logined and try to get search page-----------------------"
        time.sleep(10*random.random())
    except Exception,r:
        print '*******************************login('+username+') fail******************************'
        print Exception,":",r
        print '*******************************login('+username+') fail******************************'
