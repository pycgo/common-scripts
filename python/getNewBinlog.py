"""
文件片段 ,"position":{"file":"mysql-bin.000369","pos":4,"snapshot":true},"databaseName":
"""

import re

# 获取bin pos
def getBinPos(filepath):

    dict_binpos = {}

    patten = rb'"file":"([^"]+)","pos":(\d+)'

    with open("/Users/zxx/Documents/file","rb") as f:
        for line in f:
            match = re.findall(patten,line)
            if len(match) != 0:
                for i in match:
                    mysqlbin = i[0].decode(encoding="utf-8")
                    pos = i[1].decode(encoding="utf-8")
                    if mysqlbin not in dict_binpos:
                        dict_binpos[mysqlbin] = pos
                    if mysqlbin in dict_binpos and dict_binpos[mysqlbin] > pos:
                        dict_binpos[mysqlbin] = pos
    max_key = max(dict_binpos.keys())
    print(dict_binpos)
    print(max_key,dict_binpos[max_key])
    return max_key,dict_binpos[max_key]

def flushEnvironmentVariables():
    tuple_var = getBinPos("/Users/zxx/Documents/file")


if __name__ == '__main__':
    src_file_path = "/Users/zxx/Documents/file"
    flushEnvironmentVariables()




