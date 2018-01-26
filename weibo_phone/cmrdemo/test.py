# coding=utf-8
for i in range(1, 350):
    with open("/home/caimingrui/SJWJ/weibo/weibodate/" + key + '/' + str(i), 'r') as r:
        text = r.read()
        username = re.findall("<a class=\"nk\" href=\"[^<>(.*?)]\">[^<>(.*?)]</a><span class=\"ctt\">")[1]
        for name in username:
            print name