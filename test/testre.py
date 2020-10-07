# -*- codeing = utf-8 -*-
# @Time :  2020/9/27 12:29
# @Author : LiJunChao
# @File : testre.py
# @SoftWare : PyCharm

import re
#创建模式对象

# pat = re.compile("AA")#此处的AA是正则表达式
#
# m = pat.search("ABDSHHAADFA")
#search字符串呗校验的内容
#只显示第一个查找到的对象

# m = re.search("asd","Aasd")
# print(m)

# #findall()
# print(re.findall("a","AAFHAJa"))
# print(re.findall("[A-Z]","AAFHAJa"))
# print(re.findall("[A-Z]+","AAFaHAJa"))


#sub
print(re.sub("a","A","afdafaa"))#找到a用A将他替换在第三个字符串替换
#建议在正则表达式中，被比较的字符串前面加上r，不应担心转义字符的问题