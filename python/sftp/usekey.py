import paramiko
import os
from datetime import datetime
# 创建一个SSHClient对象
ssh = paramiko.SSHClient()
# 自动添加策略，用于保存服务器的主机名（hostname）和密钥信息，
# 如果服务器的主机名（hostname）和密钥信息没有保存在known_hosts文件中，没有这一步会无法连接。
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 加载系统SSH配置中的公钥
ssh.load_system_host_keys()

# 连接服务器，使用SSH密钥认证
ssh.connect('172.16.86.128', username='mysftp', key_filename='/Users/zxx/Documents/id_rsa')

# 创建一个SFTPClient对象
sftp = ssh.open_sftp()

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
ssh.close()
