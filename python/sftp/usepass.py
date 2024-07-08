import paramiko
import os
from datetime import datetime

# 创建一个Transport对象
transport = paramiko.Transport(("172.16.86.128", 22))

# 连接服务器，这里使用的是用户名和密码的方式，当然也可以使用秘钥的方式
transport.connect(username="mysftp", password="mysftp")

# 创建一个SFTPClient对象
sftp = paramiko.SFTPClient.from_transport(transport)

# local_dir = '/Users/zxx/PycharmProjects/pythonProject/flask8s/ftpdata'
# for file in os.listdir(local_dir):
#     # 构建完整的文件路径
#     local_file = os.path.join(local_dir, file)
#     remote_file = 'files/' + file
#
#     # 上传文件
#     sftp.put(local_file, remote_file)
#     print(f'File {file} uploaded successfully.')
# 列出目录下的所有文件
now = datetime.now()

dict_files = {}
files = sftp.listdir("files")
for file in files:
    dict_files[file.split('_')[2].split('.')[0]]=file

for key,value in dict_files.items():
    target_date = datetime.strptime(str(key), '%Y%m%d')

    delta = str(now - target_date)
    if "days" in delta:
        delta = delta.split(" ")[0]
        if int(delta) >= 7:
            dfile = dict_files[key]
            sftp.remove('files/'+dfile)


# 关闭连接
sftp.close()
transport.close()
