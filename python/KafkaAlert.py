import requests
import argparse


def args_pare():
    parser = argparse.ArgumentParser(description='kafka消费告警')
    parser.add_argument('--lag', type=int, nargs='?', default=100000,help='消费堆积数,如果大于于这个值,就告警')
    parser.add_argument('--webot_key', type=str, nargs='?', default='',help='企业微信机器人key')
    parser.add_argument('--env', type=str, nargs='?', default='', help='具体私有化环境的名称')
    parameter = parser.parse_args()
    return parameter


def send_robot(group, num, warning, key, env):
    webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + key
    if warning == 1:
        message = {"msgtype": "markdown",
                   "markdown": {"content": "{} kafka告警通知: 队列{}消息堆积量当前值为<font color=\"warning\">{}</font>".format(env, group, num), "mentioned_list": ["@all"]}}
    else:
        message = {"msgtype": "markdown",
                   "markdown": {"content": "{} kafka告警恢复通知: 队列{}消息堆积量当前值为<font color=\"info\">{}</font>".format(env, group, num),
                            "mentioned_list": ["@all"]}}
    resp = requests.post(webhook_url, json=message)
    print(resp.text)


if __name__ == "__main__":
    parameter = args_pare()
    warning_num =  parameter.lag
    old_groups = {}
    new_groups = {}
    try:
        with open('group_lag_old.txt', 'r') as f:
            for line in f:
                line_list = line.strip().split()
                old_groups[line_list[0]] = int(line_list[1])
    except:
        pass

    with open('group_lag_new.txt', 'r') as f:
        for line in f:
            line_list = line.strip().split()
            new_groups[line_list[0]] = int(line_list[1])

    for group in new_groups:
        if old_groups.get(group):
            if old_groups[group] < warning_num and new_groups[group] > warning_num:
                send_robot(group, new_groups.get(group), 1, parameter.webot_key, parameter.env)
            if old_groups.get(group) > warning_num and new_groups.get(group) < warning_num:
                send_robot(group, new_groups.get(group), 0, parameter.webot_key, parameter.env)
        #在old里面找不到记录的 超过的warning_num 要发
        else:
            if new_groups[group] > warning_num:
                send_robot(group, new_groups.get(group), 1, parameter.webot_key, parameter.env)

