# !/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# my_sender = 'cmr377256379@163.com'  # 发件人邮箱账号
# my_pass = 'hadoop123iiip'  # 发件人邮箱密码
# my_user = '377256379@qq.com'  # 收件人邮箱账号，我这边发送给自己
#
#
# def mail():
#     ret = True
#     try:
#         msg = MIMEText('Boss!!出现验证码！快点火速回来！', 'plain', 'utf-8')
#         msg['From'] = formataddr(["爬虫1出现验证码", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
#         msg['To'] = formataddr(["", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
#         msg['Subject'] = "Boss!!出现验证码！快点火速回来！"  # 邮件的主题，也可以说是标题
#
#         server = smtplib.SMTP_SSL("smtp.163.com", 994)  # 发件人邮箱中的SMTP服务器，端口是25
#         server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
#         server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
#         server.quit()  # 关闭连接
#     except Exception,e: # 如果 try 中的语句没有执行，则会执行下面的 ret=False
#         print Exception,':',e
#         ret = False
#     return ret
#
#
# ret = mail()
# if ret:
#     print("邮件发送成功")
# else:
#     print("邮件发送失败")


# cr = '[comment_id]:15647846516[/comment_id]'
# cc = re.findall('\[comment_id\]\:(.*?)\[/comment_id\]',cr)
# print cc



def a():
    try:
        a = 'dad'
        b = 123
        print a+b
    except:
        print 'dad'

def b():

    a()


def c():

    b()


if __name__ == '__main__':
    while(True):
        try:
            a()
        finally:
            print 'finally'