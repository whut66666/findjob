# -*- coding = utf-8 -*-
# @Time : 2020/10/21 19:13
# @Author : LiJunChao
# @File : test.py
# @SoftWare : PyCharm


import time
import jieba
from wordcloud import WordCloud
import re
import urllib.request,urllib.error
from jieba import analyse
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np


def main():
    url = "https://www.liepin.com/zhaopin/?"
    jobs = ['%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98',
            '%E5%9B%BE%E5%83%8F%E7%AE%97%E6%B3%95%E5%B7%A5%E7%A8%8B%E5%B8%88',
            'Java%E5%90%8E%E7%AB%AF',
            '%E4%BA%92%E8%81%94%E7%BD%91%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86'] #不同职业
    citys = ['北京', '上海', '深圳', '广州', '武汉', '杭州']
    job = ['数据挖掘', '图像算法工程师', 'java后端', '互联网产品经理']
    cityIds = ['010', '020', '050090', '050020', '170020', '070020']

    geturls(url,jobs,cityIds,citys,job)

joblink = re.compile(r'" href="(.*)" target="_blank">')   #匹配链接的正则表达式
asklink = re.compile('<div class="content content-word">[\s\S]*?(?<=任职资格|任职要求)[:：]?([\s\S]*?)(?<=<br/>)?</div>')

def geturls(url,jobs,cityIds,citys,job):
    for k in range(1,2):#0-4表示不同的职业
        for j in range(0,1):    #表示不同地区的网址0-6
            urls = url + 'key=' + jobs[k] + '&dqs=' + cityIds[j]
            getData(urls,job[k],citys[j])

def askurl(urls):
    try:
        head = {
            #"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)"
            #"User-Agent": "SafariWin7:Mozilla / 5.0(WindowsNT6.1;WOW64) AppleWebKit / 534.50(KHTML, likeGecko) Version / 5.1Safari / 534.50"
            "User-Agent":"Mozilla / 5.0(WindowsNT6.1;WOW64) AppleWebKit / 535.1(KHTML, likeGecko) Chrome / 14.0.835.163Safari / 535.1"
        }
        urls = urllib.request.Request(urls,headers=head)
        #urls = urllib.request.Request(urls)
        request = urllib.request.urlopen(urls)
        html = request.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


#筛选出网页的网址
def getData(urls,jobs,city):
    zhaopin = []
    for i in range(0, 1):  # 表示不同页数0-10
        urls = urls + '&curPage=' + str(i)
        html = askurl(urls)  # 将生成的网址传到askurl获取网页信息
        print(html)
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="job-info"):
            #print(item)
            item = str(item)    #findall函数只能用字符串
            wz = re.findall(joblink,item)
            wz = wz[0].replace("[,',]", "")  # 去掉括号和双引号
            wz = str(wz)    #将网址改成字符串用来匹配和存入列表
            if wz.find("https") == -1:   #将不符合规则的网址加上前缀存入
                wz = 'http://www.liepin.com/' + wz
                zhaopin.append(wz)
            else:
                zhaopin.append(wz)
            time.sleep(0.2)
            #print(wz)
    # require = []
    saveData(zhaopin)   #保存网址到zhaopin.txt
    findask(zhaopin)    #寻找招聘要求
    creatwordcloud(jobs,city)  # 生成词云



#保存招聘网址
def saveData(zhaopin):
    filepath = "zhaopin.txt"
    f = open(filepath,"w")
    for i in range(len(zhaopin)):
        f.write(zhaopin[i]+'\n')
    f.close()


def findask(zhaopin):
    require = []
    f = open("ask.txt","w")
    for i in range(len(zhaopin)):
        urls = zhaopin[i]
        html = askurl(urls)
        #print(html)
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="job-item main-message job-description"):
            item = str(item)
            ask = re.findall(asklink, item)
            ask = str(ask)
            #print(ask)
            ask = re.sub("[\[\]\']","",ask)
            ask = ask.replace("<br/>",'\n')
            ask = ask.replace(r"\r\n","")
            ask = ask.replace(r'\n',"")
            ask = ask.replace(r"\t","")
            f.write(ask.encode("gbk","ignore").decode("gbk","ignore"))
            f.write('\n')
            require.append(ask)
    f.close()

    clean(require)#清洗数据

def clean(require):
    f = open("last.txt","w")
    #f1 = open("keywords.txt","w")
    for i in range(len(require)):
        # 去除序号与结尾
        require[i] = re.sub(r'([0-9 a-z]+[\.\、,，)）])|（ [0-9]+ ）|[;；]', '',require[i])
        # 去除不重要的标点
        require[i] = re.sub(r'[，、。【】（）/]', ' ',require[i])
        require[i] = require[i].replace("xa0","")
        f.write(require[i].encode("gbk","ignore").decode("gbk","ignore"))
    f.close()

    #require = str(require)
    # # 筛选TF-IDF
    # keywords = jieba.analyse.extract_tags(require, topK=100, withWeight = False)
    # f1.write(str(keywords))

    #f1.close()

def creatwordcloud(jobs,city):
    f = open("last.txt","r").read()

    # 筛选TF-IDF
    keywords = jieba.analyse.extract_tags(f, topK=100, withWeight=False)
    keywords = str(keywords)
    keywords = re.sub("[\[\]\']","",keywords)

    #用关键词生成词云
    img = Image.open('底布.png')
    img_array = np.array(img)
    font_path = "C:\Windows\Fonts\simfang.ttf"
    cloud = WordCloud(font_path = font_path,
                      background_color = 'white',
                      mask = img_array).generate(keywords)

    #绘制图片
    fig = plt.figure(1)
    plt.imshow(cloud)
    plt.axis
    cloud.to_file('%s%s.jpg'%(jobs,city))

if __name__ == '__main__':
    main()
