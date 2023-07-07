import requests
import argparse
import sqlite3


def args_pare():
    parser = argparse.ArgumentParser(description='kafka消费告警')
    parser.add_argument('--lag', type=int, nargs='?', default=100000,help='消费堆积数,如果大于于这个值,就告警')
    parser.add_argument('--webot_key', type=str, nargs='?', default='ba7817ca-994e-4969-b391-1968dd9ab18c',help='企业微信机器人key')
    parser.add_argument('--env', type=str, nargs='?', default='test', help='具体私有化环境的名称')
    parameter = parser.parse_args()
    return parameter


def send_robot(group, num, warning, key, env):
    webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + key
    if warning == 1:
        message = {"msgtype": "markdown",
                   "markdown": {"content": "{} kafka告警: 队列{}消息堆积量当前值为<font color=\"warning\">{}</font>".format(env, group, num), "mentioned_list": ["@all"]}}
    elif warning == 2:
        message = {"msgtype": "markdown",
                   "markdown": {"content": "{} <font color=\"warning\">repeat</font> kafka告警: 队列{}消息堆积量当前值为<font color=\"warning\">{}</font>".format(env, group, num), "mentioned_list": ["@all"]}}
    else:
        message = {"msgtype": "markdown",
                   "markdown": {"content": "{} kafka告警恢复通知: 队列{}消息堆积量当前值为<font color=\"info\">{}</font>".format(env, group, num),
                            "mentioned_list": ["@all"]}}
    resp = requests.post(webhook_url, json=message)
    print(resp.text)

# def create_db():
#     conn = sqlite3.connect('test.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE LAG
#            (GROUPNAME           TEXT    NOT NULL,
#            LAG            TEXT     NOT NULL,
#            COUNT        INT NOT NULL);''')
#     print("数据表创建成功")
#
#     conn.commit()
#     conn.close()

if __name__ == "__main__":
    # create_db()
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

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

                c.execute("INSERT INTO LAG (GROUPNAME,LAG,COUNT) VALUES (?,?,?)", (group, new_groups.get(group), 0))
                conn.commit()
                send_robot(group, new_groups.get(group), 1, parameter.webot_key, parameter.env)
            if old_groups.get(group) > warning_num and new_groups.get(group) < warning_num:
                send_robot(group, new_groups.get(group), 0, parameter.webot_key, parameter.env)
            if old_groups.get(group) > warning_num and new_groups.get(group) > warning_num:
                c.execute("UPDATE LAG SET LAG = ?, COUNT = COUNT + 1 WHERE GROUPNAME = ?", [new_groups.get(group),group,])
                conn.commit()
                cursor = c.execute("SELECT *  from LAG")
                for row in cursor:
                    if row[0] == group and row[2] >= 5:
                        send_robot(group, new_groups.get(group), 2, parameter.webot_key, parameter.env)
                        c.execute("UPDATE LAG SET LAG = ?, COUNT = ? WHERE GROUPNAME = ?",
                                  [new_groups.get(group), 0, group, ])
                        conn.commit()

        #在old里面找不到记录的 超过的warning_num 要发
        else:
            if new_groups[group] > warning_num:
                send_robot(group, new_groups.get(group), 1, parameter.webot_key, parameter.env)
    conn.close()
