'''
检查https到期时间 做告警
todo:
   webotkey 打包的话 需要自行设置为必选参数，不给默认值，这样打包发出去才不会骚扰自己默认的机器人 如果不打包 直接改代码 就没关系
'''
from datetime import datetime, timedelta
from socket import socket
import requests
from OpenSSL import SSL
import idna
import argparse


#设置命令行可选参数
# --可选参数 不加--必选参数
def args_pare():
    parser = argparse.ArgumentParser(description='返回网站证书剩余时间')
    parser.add_argument('--fire_day', type=int, nargs='?', default=2000,help='天数,如果到期时间小于这个值,就告警')
    parser.add_argument('webot_key', type=str, nargs='?', default='',help='企业微信机器人key')
    parser.add_argument('--path',type=str, nargs='?', default='domain.txt',help='域名文件路径。默认当前路径domain.txt,可以全覆盖')
    parser.add_argument("--log", action='store_true',help='是否打印日志。默认不加参数不打印')
    parameter = parser.parse_args()
    return parameter


#获取过期时间
def get_expire_day(hostname):

    try:
        sock = socket()
        # sock.settimeout(10)   # 不要开启
        sock.setblocking(True)  # 关键
        sock.connect((hostname, 443), )
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.check_hostname = False
        ctx.verify_mode = SSL.VERIFY_NONE

        sock_ssl = SSL.Connection(ctx, sock)
        sock_ssl.set_tlsext_host_name(idna.encode(hostname))  # 关键: 对应不同域名的证书
        sock_ssl.set_connect_state()
        sock_ssl.do_handshake()

        cert = sock_ssl.get_peer_certificate()
        sock_ssl.close()
        sock.close()

        datetime_end = datetime.strptime(cert.get_notAfter().decode()[0:-1], '%Y%m%d%H%M%S')
        # 小时加8
        datetime_end = (datetime_end + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        # 转回datetime 计算用
        datetime_end = datetime.strptime(datetime_end, "%Y-%m-%d %H:%M:%S")

    except:
        datetime_end = 'get time error'
    return datetime_end


#发送告警
def sendWechatBot(content,key):
    headers = {"Content-Type": "text/plain"}
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
        }
    }

    responde = requests.post(
        url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + key,
        headers=headers, json=data)
    return responde


if __name__ == '__main__':
    domain_list = []
    content = []
    parameter = args_pare()
    with open(parameter.path,'r',encoding="utf-8") as f:
        for line in f:
            hostname = line.strip()
            domain_list.append(hostname)

    for hostname in domain_list:
        expire_time = get_expire_day(hostname)

        if isinstance(expire_time,datetime):
            expire_days = (expire_time - datetime.now()).days
        else:
            expire_days = ''

        compare_day = parameter.fire_day
        if expire_days < compare_day:
            tmp_data = hostname + '： ' + '证书剩余' + str(expire_days) + '天'
            content.append(tmp_data)

        # 是否打印日志
        if parameter.log:
            print('域名：{0},到期时间：{1},剩余{2}天'.format(hostname,expire_time,expire_days))

    if len(content) > 0 and parameter.webot_key != '':
        sendWechatBot('\n'.join(content),parameter.webot_key)
