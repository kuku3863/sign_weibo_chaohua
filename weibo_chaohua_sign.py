import json
import requests
import re
import os
from urllib.parse import urlparse, parse_qs
import time

# 定义常量
API_TEST_URL = "https://api.weibo.cn"
API_URL = "https://api.weibo.cn/2/cardlist"
SIGN_URL = "https://api.weibo.cn/2/page/button"

headers = {
    "Accept": "*/*",
    "User-Agent": "Weibo/81434 (iPhone; iOS 17.0; Scale/3.00)",
    "SNRT": "normal",
    "X-Sessionid": "6AFD786D-9CFA-4E18-BD76-60D349FA8CA2",
    "Accept-Encoding": "gzip, deflate",
    "X-Validator": "QTDSOvGXzA4i8qLXMKcdkqPsamS5Ax1wCJ42jfIPrNA=",
    "Host": "api.weibo.cn",
    "x-engine-type": "cronet-98.0.4758.87",
    "Connection": "keep-alive",
    "Accept-Language": "en-US,en",
    "cronet_rid": "6524001",
    "Authorization": "WB-SUT _2A95JzzZEDeRxGeNO6FQX8yvMyTuIHXVo3c6MrDV6PUJbkdANLWjVkWpNTxXdJQPElGxgBLb5-M-V2d2aGygXUcYb",
    "X-Log-Uid": "5036635027",
}


def check_url_access(url, headers=None, max_retries=5, wait_time=5):
    """
    检查URL是否可以访问

    :param url: 需要检查的URL
    :param headers: 请求头部，如果有的话
    :param max_retries: 最大重试次数
    :param wait_time: 两次重试之间的等待时间（秒）
    :return: True 如果URL可以访问，否则False
    """
    for i in range(max_retries):
        try:
            response = requests.get(API_TEST_URL, headers=headers, timeout=10)
            # 如果HTTP响应码在200-299之间，说明请求成功
            if 200 <= response.status_code < 300:
                return True
        except requests.RequestException:
            # 如果请求出错，等待指定的时间后再次尝试
            if i < max_retries - 1:
                time.sleep(wait_time)
                continue
            else:
                raise
    return False


def extract_params(url):
    # 解析URL
    parsed_url = urlparse(url)

    # 提取查询参数
    params_from_cookie = parse_qs(parsed_url.query)

    # 将列表值转换为单个值
    params_from_cookie = {k: v[0] for k, v in params_from_cookie.items()}

    return params_from_cookie


# 获取超话列表
def get_topics(params, headers):
    response = requests.get(API_URL, params=params, headers=headers)
    data = json.loads(response.text)

    cards = data.get("cards", [])
    topics = []
    for card in cards:
        if card.get("card_type") == "11":
            card_group = card.get("card_group", [])
            for item in card_group:
                if item.get("card_type") == "8":
                    sign_action = None
                    if "buttons" in item and len(item["buttons"]) > 0:
                        button = item["buttons"][0]
                        if "params" in button and "action" in button["params"]:
                            sign_action = button["params"]["action"]

                    topic = {
                        "title": item.get("title_sub"),
                        "desc": item.get("desc1"),
                        "sign_status": item.get("buttons", [{}])[0].get("name", ""),
                        "sign_action": sign_action
                        if item.get("buttons", [{}])[0].get("name", "") != "已签"
                        else "",
                    }

                    topics.append(topic)
    output = ""
    for topic in topics:
        output += "超话标题:'{}'，状态:'{}'\n".format(topic["title"], topic["sign_status"])

    print(output)
    return topics


# 超话签到
def sign_topic(title, action, params, headers):
    action = re.search(r"request_url=(.+)", action).group(1)
    params["request_url"] = action
    resp = requests.get(SIGN_URL, params=params, headers=headers)
    # print('服务器返回信息:', resp.json())
    if resp.json().get("msg") == "已签到":
        output = "超话标题:'{}'，状态:'签到成功！'\n".format(title)
        print(output)
    else:
        print("签到失败!")


if __name__ == "__main__":
    if check_url_access(API_TEST_URL, headers):
        params = extract_params(os.getenv("weibo_my_cookie"))
        topics = get_topics(params, headers)
        for topic in topics:
            if topic.get("sign_action") != "":
                action = topic.get("sign_action")
                title = topic.get("title")
                sign_topic(title, action, params, headers)
    else:
        print("URL无法访问，请检查网络连接或URL是否正确。")
