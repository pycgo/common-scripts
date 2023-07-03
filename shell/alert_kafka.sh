#!/bin/bash
cd /opt
for group in `kubectl -n linkflow exec -it  kafka-0 -- /opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list|dos2unix`;do 
    sum=`kubectl -n linkflow exec -it  kafka-0 -- /opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group $group|grep -v LAG|awk 'BEGIN{sum=0;}{sum+=$6}END {print sum}'`
    if [ $sum -gt 100 ];then
       echo $group $sum
    fi
done > group_lag_new.txt
# kafkaAlert是python脚本打包的工具
/usr/local/bin/kafkaAlert --webot_key=ba7817ca-994e-4969-b391-1968dd9ab18c --lag=20 --env=蒙牛生产
cp group_lag_new.txt group_lag_old.txt
