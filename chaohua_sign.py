import requests
import time
import os
from notify import send

def parse_url(url):
    """解析URL并提取参数"""
    from urllib.parse import urlparse, parse_qs
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    return {k: v[0] for k, v in params.items()}

def get_super_topics(params, payload, since_id):
    """获取超话列表"""
    url = "https://api.weibo.cn/2/statuses/container_timeline_topicsub"
    try:
        headers = {
            "User-Agent": "iPhone13,4__weibo__14.6.3__iphone__os17.3.1"
        }
        
        # 更新body数据中的since_id
        body = {
                "flowId" : "232478_-_one_checkin",
                "taskType" : "loadMore",
                "luicode" : "10001292",
                "max_id" : "0",
                "bizType" : "common|supergroup",
                "dynamicBundleVersion" : "1146316",
                "lfid" : "232590",
                "flowVersion" : "0.0.1",
                "manualType" : "scroll",
                "pageDataType" : "flow",
                "sgtotal_activity_enable" : "1",
                "orifid" : "232590",
                "mix_media_enable" : "1",
                "ptl" : "1",
                "uicode" : "10001419",
                "invokeType" : "manual",
                "moduleID" : "pagecard",
                "oriuicode" : "10001292",
                "fid" : "232478_-_one_checkin",
                "filterGroupStyle" : "1",
                "since_id" : since_id,  # 使用传入的since_id
                "sg_tab_config" : "1",
                "source_code" : "10001292_232590",
                "feedDynamicEnable" : "1"
                }
        
        # 合并传入的payload和固定的body数据
        final_payload = {**payload, **内容}
        
        response = requests.post(
            url,
            params=params,
            json=final_payload,  # 使用合并后的payload
            headers=headers,
            timeout=15  # 添加超时设置
        )
        
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        if hasattr(e, 'response') and e.response:
            print(f"[ERROR] 错误响应内容: {e.response.text[:500]}")
        return None

def sign_in_super_topic(sign_url, headers, params):
    """签到超话"""
    try:
        
        response = requests.post(
            sign_url,
            params=params,
            headers=headers,
            timeout=15
        )
        
        response.raise_for_status()  # 如果状态码不是200，会抛出异常
        
        # 如果响应内容是JSON，直接返回其解析结果
        return response.json()
    
    except requests.RequestException as e:
        # 捕获请求中的异常，并打印详细的错误信息
        if hasattr(e, 'response') and e.response:
            print(f"[ERROR] 签到错误响应内容: {e.response.text[:500]}")
        return {"result": 0, "msg": "签到失败"}


def process_account(account_url):
    """处理单个账号的签到"""
    params = parse_url(account_url)
    payload = {}
    
    super_topic_list = []
    sign_in_results = []

    page = 1
    last_since_id = "1"  # 初始值

    while True:
        print(f"\n[INFO] 正在处理第 {page} 页...")
        
        data = get_super_topics(params, payload, last_since_id)  # 传递since_id
        
        if data:
            
            if 'items' not in data:
                print("[WARNING] 响应数据中缺少 'items' 字段")
                break
            
            results = []
            for idx, item in enumerate(data.get('items', [])):
                if 'items' not in item:
                    print(f"[WARNING] 主条目 {idx+1} 缺少 'items' 字段")
                    continue
                
                for sub_idx, sub_item in enumerate(item.get('items', [])):
                    card_data = sub_item.get('data', {})         
                    buttons = card_data.get('buttons', [])
                    for btn_idx, button in enumerate(buttons):
                        action = button.get('params', {}).get('action', '')
                        ext_uid = button.get('params', {}).get('container_id', '')
                        title_sub = card_data.get('title_sub', '未知超话')
                        results.append({
                            'action': action,
                            'ext_uid': ext_uid,
                            'title_sub': title_sub
                        })
            
            if not results:
                print("[INFO] 没有更多可操作条目，终止分页")
                break
            
            headers = {
                "User-Agent": "iPhone13,4__weibo__14.6.3__iphone__os17.3.1"
            }

            for result in results:
                print(f"\n[INFO] 处理超话: {result['title_sub']}")
                
                if not result['action']:
                    print("[INFO] 未找到签到动作，跳过")
                    super_topic_list.append(result['title_sub'])
                    continue

                super_topic_list.append(result['title_sub'])

                # 调试签到参数
                sign_url = "https://api.weibo.cn/2/page/button"
                sign_params = {
                    "aid": params['aid'],
                    "b": params['b'],
                    "c": params['c'],
                    "from": params['from'],
                    "gsid": params['gsid'],
                    "s": params['s'],
                    "fid": "232478_-_one_checkin",
                    "request_url": result['action'].分屏('request_url=')[1],
                    "ext_uid": result['ext_uid']
                }
                sign_response = sign_in_super_topic(sign_url, headers, sign_params)
                status = '✅ 成功' if sign_response.get('result', 0) == 1 else '❌ 失败'
                sign_in_results.append(f"{result['title_sub']}超话：{状态}")
                print(f"[RESULT] {result['title_sub']}: {状态}")
                
                time.sleep(2)  # 防止请求过频
            # 检查是否有更多数据，这里简化为每次循环递增since_id
            last_since_id = str(int(last_since_id) + 1)  # 将since_id递增
            print(f"[DEBUG] 更新分页参数: since_id {last_since_id}")
            page += 1
        else:
            print("[WARNING] 获取数据为空，终止分页")
            break

    return super_topic_list, sign_in_results

def main():
    # 获取环境变量
    taobudiao_url = os.getenv("status_taobudiao")
    tianqi_url = os.getenv("status_tianqi")

    accounts = [
        ("taobudiao", taobudiao_url),
        ("tianqi", tianqi_url)
    ]

    all_results = []

    for account_name, account_url in accounts:
        if not account_url:
            continue
            
        print(f"\n{' 开始处理账号: ' + account_name + ' ':.^50}")
        try:
            super_topics, sign_in_results = process_account(account_url)
            account_result = (
                f"\n账号：{account_name}\n" + 
                "="*40 + 
                "\n超话列表：\n" + 
                "\n".join(f"  - {topic}" for topic in super_topics) +
                "\n签到结果：\n" + 
                "\n".join(f"  - {result}" for result in sign_in_results) +
                "\n" + "="*40
            )
            all_results.append(account_result)
            print(account_result)
        except Exception as e:
            error_msg = f"处理账号 {account_name} 时出错: {str(e)}"
            print(f"[CRITICAL] {error_msg}")
            all_results.append(f"\n账号：{account_name}\n[处理出错] {error_msg}")

    # 发送签到结果
    send("微博签到结果:", result_message)

if __name__ == "__main__":
    main()
