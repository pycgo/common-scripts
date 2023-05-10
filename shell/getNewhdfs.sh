#/bin/bash
rm -f /opt/_metadata
newpath=`hdfs dfs -ls /flink/mysql-cdc | sort -k 6,7 | tail -n 1|awk '{print $8}'`
downpath=`hdfs dfs -ls $newpath | sort -k 6,7 | tail -n 1|grep chk|awk '{print $8}'`
hdfs dfs -get $downpath/_metadata
