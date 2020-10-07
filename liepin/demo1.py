# -*- codeing = utf-8 -*-
# @Time :  2020/9/27 17:41
# @Author : LiJunChao
# @File : demo1.py
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
    cityIds = ['010', '020', '050090', '050020', '170020', '070020']
    zhaopin = []    #存储招聘信息的网址
    # require = []
    filepath = "zhaopin.txt"
    zhaopin = getData(url,zhaopin,filepath,citys,jobs,cityIds)  #信息筛选
    # saveData(zhaopin,filepath)      #保存信息
    # require = findask(zhaopin,require)                #寻找招聘要求
    # clean(require)          #清洗数据
    # creatwordcloud()            #生成词云


joblink = re.compile(r'" href="(.*)" target="_blank">')   #匹配链接的正则表达式
asklink = re.compile('<div class="content content-word">[\s\S]*?(?<=任职资格|任职要求)[:：]?([\s\S]*?)(?<=<br/>)?</div>')

def askurl(urls):
    try:
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        }
        urls = urllib.request.Request(urls,headers=head)
        request = urllib.request.urlopen(urls)
        html = request.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return  html


def getData(url,zhaopin,filepath,citys,jobs,cityIds):
    for k in range(3,4):#0-4
        for j in range(0,6):    #表示不同地区的网址0-6
            for i in range(0,10):    #表示不同页数0-10
                urls = url + 'key=' + jobs[k] + '&dqs=' + cityIds[j] + '&curPage=' + str(i)
                # print(urls)
                html = askurl(urls)
                # print(html)
                soup = BeautifulSoup(html,"html.parser")
                for item in soup.find_all('div',class_="job-info"):
                    # print(item)
                    item = str(item)    #findall函数只能用字符串
                    wz = re.findall(joblink,item)
                    wz = wz[0].replace("[,',]", "")  # 去掉括号和双引号
                    wz = str(wz)    #将网址改成字符串用来匹配和存入列表
                    if wz.find("https") != -1:   #将不符合规则的网址加上前缀存入
                        zhaopin.append(wz)
                    time.sleep(0.2)
                    # print(wz)
            require = []
            saveData(zhaopin,filepath)
            require = findask(zhaopin, require)  # 寻找招聘要求
            clean(require)  # 清洗数据
            creatwordcloud(citys[j])  # 生成词云
            zhaopin = []
            time.sleep(2)


    return zhaopin

#保存招聘网址
def saveData(zhaopin,filepath):
    f = open(filepath,"w")
    for i in range(len(zhaopin)):
        f.write(zhaopin[i]+'\n')
    f.close()


def findask(zhaopin,require):
    f = open("ask.txt","w")
    for i in range(len(zhaopin)):
        url = zhaopin[i]
        html = askurl(url)
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
    return require

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

def creatwordcloud(city):
    f = open("last.txt","r").read()
    # 筛选TF-IDF
    keywords = jieba.analyse.extract_tags(f, topK=100, withWeight=False)
    keywords = str(keywords)
    keywords = re.sub("[\[\]\']","",keywords)

    #用关键词生成词云
    img = Image.open('timg.jpg')
    img_array = np.array(img)
    font_path = "C:\Windows\Fonts\simfang.ttf"
    cloud = WordCloud(font_path = font_path,
                      background_color = 'white',
                      mask = img_array).generate(keywords)

    #绘制图片
    fig = plt.figure(1)
    plt.imshow(cloud)
    plt.axis
    print("互联网产品经理%s地区的云图已经生成"%city)
    cloud.to_file('互联网产品经理%s.jpg'%city)

if __name__ == '__main__':
    main()