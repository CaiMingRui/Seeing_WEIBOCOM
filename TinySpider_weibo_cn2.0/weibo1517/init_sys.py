# coding=utf-8

import os
from xml.dom import minidom
import xml.dom.minidom

def init_sys(str_conf_fp):
    dict = {}
    if(os._exists(str_conf_fp)):
        dom = xml.dom.minidom.parse(str_conf_fp)
        root=dom.documentElement
        dict["ReadMname"] = root.getElementsByTagName('ReadMname')[0]
        dict["SaveMname"] = root.getElementsByTagName('SaveMname')[0]
        dict["movie_html_page"] = root.getElementsByTagName('movie_html_page')[0]
        dict["save_Name_url"] = root.getElementsByTagName('save_Name_url')[0]
        dict["save_userpage"] = root.getElementsByTagName('save_userpage')[0]
    return dict

