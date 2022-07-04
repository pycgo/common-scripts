# 每台机器都有/var/log/hadoop/hdfs 和/var/log/hive 做一个定时清理三天前的日志
# crontab参考
# 1 20 * * * /bin/bash /opt/truncate_hdp_log.sh >/dev/null 2>&1
#!/bin/bash
find /var/log/hadoop/hdfs -type f -mtime +3 |grep hdfs-audit.log| xargs rm
find /var/log/hive -type f -mtime +3| xargs rm
 
 
