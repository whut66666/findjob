# -*- codeing = utf-8 -*-
# @Time :  2020/9/27 14:21
# @Author : LiJunChao
# @File : textxlwt.py
# @SoftWare : PyCharm

import xlwt

workbook = xlwt.Workbook(encoding="utf-8")#创建workbook对象
worksheet = workbook.add_sheet('sheet1')#创建工作表
# for i in range(0,9):
#     for j in range(0,i+1):
#         worksheet.write(i,j,"%d*%d=%d"%(i+1,j+1,(i+1)*(j+1)))
# workbook.save('chengfa.xls')
# worksheet.write(0,0,'hello')        #写入数据
# workbook.save('student.xls')        #保存数据表
