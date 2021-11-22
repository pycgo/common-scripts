import os
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json

#shell 生成数据 在linux 直接用shell 不用这个函数
'''
#! /bin/bash
cd /root/gitee/jd_docker && /usr/local/git/bin/git pull > /root/gitee/git
echo $?
python3 /root/gitee/update_notice.py
'''
def createGitData():
    os.system('git pull > git')


#处理数据
def getGitUpdate():
    set1 = set()
    with open('/root/gitee/git', 'r') as f:
        for line in f:
            list_line = line.split('|')

            if len(list_line) == 2:
                set1.add(list_line[0].strip())
    return set1

#企业微信机器人
def sendWechatBot(key,content):
    headers = {"Content-Type": "text/plain"}
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
        }
    }
    r = requests.post(
        url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + key,
        headers=headers, json=data)
    print(r.text)

#钉钉机器人
def sendDingBot(access_token,secret,content):
    secret_enc = secret.encode('utf-8')
    timestamp = str(round(time.time() * 1000))
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    webhook = "https://oapi.dingtalk.com/robot/send?access_token=%s&timestamp=%s&sign=%s" %(access_token,timestamp,sign)
    header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
    }
    message = {
                "msgtype": "text",
                "text": {
                    "content": content
                },
                "at": {
                    "atMobiles": [""],
                    "isAtAll": False
                }
    }

    message_json = json.dumps(message)
    res = requests.post(url=webhook,data=message_json,headers=header)
    return res.text


if __name__ == "__main__":
    #企业微信机器人信息
    key = 'xxx-cf4fa-769b-4267-xxx'

    # 钉钉机器人信息
    access_token = '06e92980d6ebe62b754ce7a53e07---xxx'
    secret = 'SECb2625fbeb96422dd86db07a277faa1b---xxx'

    # text
    message =  getGitUpdate()
    if len(message) >= 1:

        content = "脚本有更新："+ '\n'+ str(getGitUpdate())
        sendWechatBot(key,content)
        sendDingBot(access_token, secret, content)


