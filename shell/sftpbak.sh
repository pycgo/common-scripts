#!/bin/bash
#备份sftp服务端的某个目录数据
today=`date +%Y_%m_%d`
mkdir -p /opt/sftpbak
cd /opt/sftpbak
mkdir -p $today

#用户名
GET_USER=
#IP
GET_IP=
GET_PORT=22
#密码
GET_PASSWORD=
#sftp需要备份的目录
GET_DATA_PATH=


sftp_download()
{
    expect <<- EOF
    set timeout 5
    spawn sftp  -P $GET_PORT $GET_USER@$GET_IP
 
    expect { 
        "(yes/no)?" { send "yes\r"; exp_continue}
        "*assword:" { send "$GET_PASSWORD\r"}
    }
    expect "sftp>"
    send "get -r $GET_DATA_PATH $today/$GET_DATA_PATH\r"
    expect "sftp>"
    send "bye\r"
EOF
}
sftp_download
