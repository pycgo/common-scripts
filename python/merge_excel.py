#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import xlsxwriter
import os
import logging
import sys


# 获取所有excle文件列表的方法 可以同目录,也支持子目录
def file_list(path):
    filelist = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if "xls" in name and name != "chart.xlsx":
                filelist.append(name)
    return filelist


# 定义一个读写excle方法
def handel_excle():
    path = '.'
    filelist = file_list(path)
    
	  #新建要存结果的excle，可以自己改其他路径
    workbook = xlsxwriter.Workbook('chart.xlsx')
    worksheet = workbook.add_worksheet()
    for file in filelist:
        data = xlrd.open_workbook(file)
        #获取指定Sheet的名字
        sheet = data.sheet_by_name(u'Sheet1')
        #获取总行数
        #nrows = sheet.nrows
        #读取第一行的数据 0是第一行  1是第二行  以此类推
        first_row = sheet.row_values(0)
        count = filelist.index(file) + 1
        worksheet.write_row('A'+str(count), first_row)
    workbook.close()


def main():
    file_path = r'.'
    file_list(file_path)
    handel_excle()


if __name__ == '__main__':
    try:
        reload(sys)
        sys.setdefaultencoding("utf-8")
        main()
    except Exception as e:
        logging.error(e)
        os._exit(-1)
