import os
import zipfile


# 获取zip 文件 解压zip包
def unzip_file(zip_file_path,unzip_dest_path):
    if not os.path.exists(unzip_dest_path):
        os.makedirs(unzip_dest_path)
    for root, dirs, files in os.walk(zip_file_path):
        for name in files:
            if name.endswith('.zip'):
                zip_file_name = os.path.join(zip_file_path, os.path.join(root, name))
                filezip = zipfile.ZipFile(zip_file_name)
                out_unzip_path = os.path.join(unzip_dest_path,name.strip('.zip'))
                if not os.path.exists(out_unzip_path):
                    os.makedirs(out_unzip_path)
                filezip.extractall(path=out_unzip_path)
