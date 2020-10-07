# -*- codeing = utf-8 -*-
# @Time :  2020/9/27 9:18
# @Author : LiJunChao
# @File : testUrllib.py.py
# @SoftWare : PyCharm

import urllib.request

#获取一个get请求
# response = urllib.request.urlopen("http://www.baidu.com")
#response = urllib.request.urlopen("https://m.liepin.com/zhaopin/?degradeFlag=0&key=%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98&dqs=010")
#print(response.read().decode('utf-8'))  #对获取的网页源码进行utf-8解码


#获取一个post请求（用来封装用户名和密码和cookie来模仿访问网站18集18分钟）
#import urllib.parse
# response = urllib.request.urlopen("")


#解决超时问题（"User-Agent": "Python-urllib/3.8"显示爬虫，网站可以采取措施超时）
# try:
#     response = urllib.request.urlopen("http://httpbin.org/get",timeout=0.01)
#     print(response.read().decode('utf-8'))
# except urllib.error.URLError as e:
#     print("time out!")

# response = urllib.request.urlopen("http://www.baidu.com")#418发现爬虫，414找不到
#print(response.getheaders())获取信息
#print(response.getheader("Server"))获取单个信息


#访问豆瓣需要封装
# url = "http://www.douban.com"
# headers={
# "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36"
# }
# #req = urllib.request.Request(url=url,data=data,headers=headers,method="POST")
# req = urllib.request.Request(url=url,headers=headers)
# response = urllib.request.urlopen(req)
# print(response.read().decode("utf-8"))
