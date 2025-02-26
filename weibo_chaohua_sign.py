import json
import requests
import random
import time
from urllib.parse import urlparse, parse_qs
from notify import send
import re
import os

API_URL = "https://api.weibo.cn/2/cardlist"
SIGN_URL = "https://api.weibo.cn/2/page/button"

def send_request(url, params, headers):
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return None
    return None

def extract_params(url):
    parsed_url = urlparse(url)
    params_from_url = parse_qs(parsed_url.query)
    params_from_url = {k: v[0] for k, v in params_from_url.items()}
    return params_from_url

def get_card_type_11(params, headers, since_id):
    params['since_id'] = since_id  # 添加 since_id 到请求参数中
    data = send_request(API_URL, params, headers)
    if data is None:
        return []
    cards = data.get("cards", [])
    card_type_11_info = []
    for card in cards:
        if card.get("card_type") == 11:
            card_group = card.get("card_group", [])
            for item in card_group:
                if item.get("card_type") == 8:
                    info = {
                        "scheme": item.get("scheme"),
                        "title_sub": item.get("title_sub")
                    }
                    card_type_11_info.append(info)
    return card_type_11_info

def sign_in(headers, base_params, scheme, since_id):
    params = extract_params(scheme)
    request_url = f"http://i.huati.weibo.com/mobile/super/active_fcheckin?cardid=bottom_one_checkin&container_id={params['containerid']}&pageid={params['containerid']}&scheme_type=1"
    sign_in_params = {
        "aid": base_params.get("aid"),
        "b": base_params.get("b"),
        "c": base_params.get("c"),
        "from": base_params.get("from"),
        "ft": base_params.get("ft"),
        "gsid": base_params.get("gsid"),
        "lang": base_params.get("lang"),
        "launchid": base_params.get("launchid"),
        "networktype": base_params.get("networktype"),
        "s": base_params.get("s"),
        "sflag": base_params.get("sflag"),
        "skin": base_params.get("skin"),
        "ua": base_params.get("ua"),
        "v_f": base_params.get("v_f"),
        "v_p": base_params.get("v_p"),
        "wm": base_params.get("wm"),
        "fid": "232478_-_one_checkin",
        "lfid": base_params.get("lfid"),
        "luicode": base_params.get("luicode"),
        "moduleID": base_params.get("moduleID"),
        "orifid": base_params.get("orifid"),
        "oriuicode": base_params.get("oriuicode"),
        "request_url": request_url,
        "since_id": since_id,
        "source_code": base_params.get("source_code"),
        "sourcetype": "page",
        "uicode": base_params.get("uicode"),
        "ul_sid": base_params.get("ul_sid"),
        "ul_hid": base_params.get("ul_hid"),
        "ul_ctime": base_params.get("ul_ctime"),
    }
    data = send_request(SIGN_URL, sign_in_params, headers)
    return data

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
    "Authorization": "",
    "X-Log-Uid": "5036635027",
}

if __name__ == "__main__":
    weibo_my_cookie = os.getenv("weibo_my_cookie")
    since_id = 1
    while True:
        params = extract_params(weibo_my_cookie)
        card_type_11_info = get_card_type_11(params, headers, since_id)  # 传递 since_id 到函数中
        
        if not card_type_11_info:  # 如果没有数据，停止循环
            break
        
        super_topic_list = "\n".join([f"    {info['title_sub']}" for info in card_type_11_info])
        print("超话列表：")
        print(super_topic_list)
        
        result_message = "\n签到结果：\n"
        for info in card_type_11_info:
            result = sign_in(headers, params, info['scheme'], since_id)
            if result and result.get('msg') == '已签到':
                status = '✅ 成功'
            else:
                status = '❌ 失败'
            result_message += f"    {info['title_sub']}超话：{status}\n"
            time.sleep(random.randint(5, 10))  
        print(result_message)
        
        since_id += 1 
