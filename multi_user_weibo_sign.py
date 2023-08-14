import json
import requests
import re
import os
import random
import time
from urllib.parse import urlparse, parse_qs
from notify import send


class WeiboSigner:
    API_URL = "https://api.weibo.cn/2/cardlist"
    SIGN_URL = "https://api.weibo.cn/2/page/button"

    def __init__(self, cookie):
        self.params = self.extract_params(cookie)
        self.headers = {
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
            "Authorization": self.generate_authorization(self.params),
            "X-Log-Uid": "5036635027",
        }

    @staticmethod
    def extract_params(cookie):
        parsed_url = urlparse(cookie)
        params_from_cookie = parse_qs(parsed_url.query)
        return {k: v[0] for k, v in params_from_cookie.items()}

    @staticmethod
    def generate_authorization(params):
        # 从参数中生成授权信息
        gsid = params.get("gsid")
        return f"WB-SUT {gsid}" if gsid else None

    def send_request(self, url, params):
        # 发送请求并处理重试逻辑
        max_retries = 15
        wait_time = 5
        for i in range(max_retries):
            try:
                response = requests.get(url, params=params, headers=self.headers)
                response.raise_for_status()
                return json.loads(response.text)
            except requests.RequestException as e:
                if i < max_retries - 1:
                    print(f"请求失败，原因: {e}。{wait_time}秒后重试...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise

    def get_username(self):
        url = 'https://api.weibo.cn/2/profile/me'
        response = self.send_request(url, self.params)
        if 'mineinfo' in response:
            return response['mineinfo']['screen_name']
        else:
            print("错误：响应中缺少 'mineinfo' 键")
            return None

    def get_since_id(self):
        # 获取since_id
        data = self.send_request(self.API_URL, self.params)
        return data["cardlistInfo"]["since_id"]

    def get_topics(self):
        # 获取超话列表
        data = self.send_request(self.API_URL, self.params)
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
                            "sign_status": item.get("buttons", [{}])[0].get("name", ""),
                            "sign_action": sign_action if item.get("buttons", [{}])[0].get("name",
                                                                                           "") != "已签" else "",
                        }
                        topics.append(topic)
        # 打印超话列表
        for topic in topics:
            print(f"超话标题: {topic['title']}, 状态: {topic['sign_status']}")

        return topics

    def sign_topic(self, title, action):
        # 超话签到
        message = ""
        action = re.search(r"request_url=(.+)", action).group(1)
        self.params["request_url"] = action
        time.sleep(random.randint(5, 10))
        resp = requests.get(self.SIGN_URL, params=self.params, headers=self.headers)
        if resp.json().get("msg") == "已签到":
            qd_output = "超话标题:'{}'，状态:'签到成功！'\n".format(title)
            print(qd_output)
            message += qd_output
        else:
            print("签到失败!")
        return message

    def main(self):

        # 创建 WeiboSigner 实例
        weibo_signer = WeiboSigner(user_cookie)
        print('用户名:', weibo_signer.get_username())
        since_id = weibo_signer.get_since_id()
        # 每页显示1000条数据
        weibo_signer.params["count"] = "1000"
        message_to_push = ""
        succeeded = False
        while not succeeded:
            try:
                while True:
                    topics = weibo_signer.get_topics()
                    if not any(topic.get("sign_action") != "" for topic in topics):
                        break
                    for topic in topics:
                        if topic.get("sign_action") != "":
                            action = topic.get("sign_action")
                            title = topic.get("title")
                            message = weibo_signer.sign_topic(title, action)
                            message_to_push += message
                succeeded = True
            except Exception as e:
                print(e)
                time.sleep(60)
        print()  # 打印一个空行
        send("微博签到结果:", message_to_push)
        print()  # 打印一个空行


if __name__ == "__main__":
    # 获取用户参数
    weibo_my_cookie = os.getenv("weibo_my_cookie")
    # weibo_my_cookie = ""
    user_cookies = weibo_my_cookie.split(';')  # 通过分号分割多个用户的 cookie
    if user_cookies is None:
        print("错误：请设置环境变量 'weibo_my_cookie'")
        exit(1)
    # 获取用户名
    for user_cookie in user_cookies:
        weibo_signer = WeiboSigner(user_cookie)  # 这里传入cookie
        weibo_signer.main()  # 或者其他调用逻辑
