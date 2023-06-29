#!/bin/bash
for i in `kubectl -n linkflow get pvc|sed 1d|awk  '{print $1}'|grep data|awk -F "data-" '{print $2}'`
do
if [[ $i =~ ^(rabbitmq|kafka|zookeeper).* ]];then
    key_path="bitnami"
else
    key_path="data"
fi
tmp_data=`kubectl -n linkflow exec -it $i -- df -h|grep $key_path|awk -F '%' '{print $1}'`
echo $tmp_data
disk_use_percent=`echo $tmp_data|awk '{print $NF}'`
disk_Avail=`echo $tmp_data|awk  '{print $4}'|awk -F 'G' '{print $1}'|awk -F '.' '{print $1}'`
if [[ $disk_use_percent -ge 85 && $disk_Avail -le 50 ]];then
    message='{"msgtype": "text", "text": {"content": "xx生产'$i'磁盘使用率'$disk_use_percent'% 正在告警,还剩余'$disk_Avail'G", "mentioned_list": ["@all"]}}'
    curl -XPOST -d "$message" https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
    echo $message
else
    echo $i 磁盘使用率$disk_use_percent% 还剩余$disk_Avail 没问题
fi
done
