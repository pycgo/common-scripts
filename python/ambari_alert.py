import argparse
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json
import os
import shutil
import time

# 暂时不用
# def args_pare():
#     parser = argparse.ArgumentParser(description='')
#     parser.add_argument('--url', type=str, nargs='?', default='',help='ambari地址')
#     parser.add_argument('--user', type=str, nargs='?', default='', help='ambari账户')
#     parser.add_argument('--passwd', type=str, nargs='?', default='', help='ambari密码')
#     parameter = parser.parse_args()
#     return parameter

def sendDingBot(access_token,secret,content,warning):
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

    if warning == 1:
        warning_color = "#FF0000"
        warning_title = "告警通知"
    if warning == 0:
        warning_color = "#32CD32"
        warning_title = "告警恢复通知"
    message_list = content.split(',')
    print("messaghe list",message_list)
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": "ambari平台告警通知",
            "text": "## <font color=%s>%s</font>" % (
            warning_color, warning_title)  +'\n\n'+ message_list[0]+'\n\n'+ message_list[1] +'\n\n' + message_list[2]},
        "isAtAll": False,
    }

    message_json = json.dumps(message)
    res = requests.post(url=webhook,data=message_json,headers=header)
    return res.text

def host_info():
    file = open(new_path,'w')
    # parameter = args_pare()
    # main_url = requests.get('http://' + parameter.url + '/api/v1/clusters', auth=(parameter.user, parameter.passwd))

    session = requests.session()
    warn = session.get('http://hdp1-test.leadswarp.com:8080/api/v1/clusters/linkflow/alerts?fields=Alert/definition_name,Alert/host_name,'
                       'Alert/instance,Alert/label,Alert/latest_timestamp,Alert/original_timestamp,Alert/service_name,Alert/state,'
                       '&Alert/state.in(CRITICAL,WARNING)&Alert/maintenance_state.in(OFF)', auth=('admin', 'admin'),verify=False)
    for warning in warn.json()["items"]:
        alert_name = "告警名称: " + warning['Alert']['label']
        alert_service = "服务名称: " + warning['Alert']['service_name']
        alert_level = "告警等级: " +  warning['Alert']['state']
        file.write(alert_name+ "," + alert_service + "," + alert_level +'\n')
    file.close()

if __name__ == "__main__":
    access_token = '14d776ee0b877f0d71a57266c3721400efe9215c914f3f932ac9100638f8033f'
    secret = 'SEC893e2903d4ec1dd2025bc168c31f53409f940cf84363dd528335baaa044bd6d8'
    new_path = 'alert_new.txt'
    old_path = 'alert_old.txt'
    host_info(new_path)
    old_groups = {}
    new_groups = {}



    # 决定是否向old_dict写数据
    try:
        with open(old_path, 'r') as f:
            for line in f:
                line_list = line.strip().split(",")
                old_groups[line_list[0]] = line_list[1:]
    except:
        pass

    size = os.path.getsize(new_path)

    #决定是否向new_dict写数据
    new_file_list = []
    if size == 0:
        pass
    else:
        with open(new_path, 'r') as f:
            for line in f:
                line_list = line.strip().split(",")
                new_groups[line_list[0]] = line_list[1:]

    if len(new_groups) == 0 and len(old_groups) == 0:
        pass
    if len(new_groups) == 0 and len(old_groups) != 0:
        for key,value in old_groups.items():
            sendDingBot(access_token,secret, key+ ',' + ','.join(list(value)),warning=0)
    if len(new_groups) != 0 and len(old_groups) == 0:
        # 1发告警  cp new.txt old.txt
        for key,value in new_groups.items():
            sendDingBot(access_token,secret,key+ ','+ ','.join(list(value)),warning=1)
        shutil.copy(new_path,old_path)
    if len(new_groups) != 0 and len(old_groups) != 0:
        #1 两个字典相同的数据  不用写
        # jiaoji = new_groups.items() & old_groups.items()
        # old存在 new不存在 告警恢复 a-b
        chaji_a_b = old_groups.keys() - new_groups.keys()
        chaji_b_a = new_groups.keys() - old_groups.keys()
        jiaoji_ab = old_groups.keys() & new_groups.keys()
        if len(chaji_a_b) != 0:
            for i in chaji_a_b:
                sendDingBot(access_token,secret,i + ','+ ','.join(old_groups[i]),warning=0)
                print("1")
        if len(chaji_b_a) != 0:
            for j in chaji_b_a:
                sendDingBot(access_token, secret, j + ','+ ','.join(new_groups[j]),warning=1)
                print("2")
        if len(jiaoji_ab) != 0:
            for x in jiaoji_ab:
                if old_groups[x] != new_groups[x]:
                    sendDingBot(access_token,secret,x + ','+ ','.join(new_groups[x]),warning=1)
                    print("3")
        shutil.copy(new_path, old_path)
