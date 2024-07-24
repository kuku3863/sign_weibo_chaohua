import requests
import time
from notify import send
import os

def parse_url(url):
    """解析URL并提取参数"""
    from urllib.parse import urlparse, parse_qs
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    return {k: v[0] for k, v in params.items()}

def get_super_topics(params, payload):
    """获取超话列表"""
    url = "https://api.weibo.cn/2/statuses/container_timeline_topicsub"
    response = requests.post(url, params=params, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None

def sign_in_super_topic(sign_url, headers, params):
    """签到超话"""
    response = requests.post(sign_url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"result": 0, "msg": "签到失败"}

def main():  
    # 解析URL并提取参数
    params = parse_url(os.getenv("status_cookie"))
    
    # 请求的payload
    payload = {}
    
    super_topic_list = []
    sign_in_results = []

    page = 1

    while True:
        data = get_super_topics(params, payload)
        
        if data and 'items' in data:
            results = []
            for item in data.get('items'， []):
                for sub_item in item.get('items'， []):
                    card_data = sub_item.get('data', {})
                    if 'buttons' in card_data:
                        for button in card_data['buttons']:
                            action = button.get('params', {})。get('action', '')
                            ext_uid = button.get('params', {})。get('container_id', '')
                            title_sub = card_data.get('title_sub', '')
                            results.append({'action': action, 'ext_uid': ext_uid, 'title_sub': title_sub})
            
            if not results:
                break
            headers = {
                "User-Agent": "iPhone13,4__weibo__14.6.3__iphone__os17.3.1"
            }

            for result in results:
                if not result['action']:
                    super_topic_list.append(result['title_sub'])
                    continue

                super_topic_list.append(result['title_sub'])

                # 签到请求参数
                sign_url = "https://api.weibo.cn/2/page/button"
                sign_params = {
                    "aid": params['aid'],
                    "b": params['b'],
                    "c": params['c'],
                    "from": params['from'],
                    "gsid": params['gsid'],
                    "s": params['s'],
                    "fid": "232478_-_one_checkin",
                    "request_url": result['action'].split('request_url=')[1],
                    "ext_uid": result['ext_uid']
                }
                sign_response = sign_in_super_topic(sign_url, headers, sign_params)
                sign_in_results.append(f"{result['title_sub']}超话：{'成功' if sign_response.get('result', 0) == 1 else '失败'}")
                time.sleep(2)  # 添加延时

            # 更新since_id以获取下一页数据
            page += 1
            params['since_id'] = f"{page}_1"
        else:
            break

   # 输出超话列表
    result_message = "\n签到结果：\n" + "\n".join(sign_in_results)
    print("超话列表：")
    for topic in super_topic_list:
        print(f"    {topic}")

    # 输出签到结果
    print(result_message)

    # 发送签到结果
    send("微博签到结果:", f"超话列表：\n{super_topic_list}\n{result_message}")

if __name__ == "__main__":
    main()
