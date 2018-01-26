# coding=utf-8

import os

for i in range(2010,2018):
    movienamels = os.listdir("/home/caimingrui/SJWJ/weibo/ActorRole/"+str(i)+"/")
    if os.path.exists("/home/caimingrui/SJWJ/weibo/weibodate/movie_time_name/"+str(i)):
        print "file is exists"
    else:
        os.mkdir("/home/caimingrui/SJWJ/weibo/weibodate/movie_time_name/"+str(i))
    with open("/home/caimingrui/SJWJ/weibo/weibodate/movie_time_name/"+str(i)+"/"+str(i),'wb') as f:
        for movie in movienamels:
            print str(i)+"add"+movie
            f.write(movie+'\n')

