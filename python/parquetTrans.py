/*
解析从hdfs下载下来的parquet类型的文件
*/
import pandas as pd
import os


filelist = []
for root, dirs, files in os.walk("/Users/zxx/zxx/django/pythonProject1/paque/default"):

    for i in files:
        filename = root +"/"+i
        print("do tans ",i)
        df = pd.read_parquet(filename)
        df.to_csv(i + '.csv')
