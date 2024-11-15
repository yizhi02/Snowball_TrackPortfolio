import requests
import time
import json
from datetime import datetime
from colorama import init, Fore, Style

# 初始化 colorama
init(autoreset=True)

# 读取配置文件
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Telegram 配置
telegram_bot_token = config['telegram_bot_token']
telegram_chat_id = config['telegram_chat_id']

# 雪球组合代码
portfolio_code = config['portfolio_code']

# 雪球 API URL
xueqiu_api_url = f'https://xueqiu.com/cubes/rebalancing/history.json?cube_symbol={portfolio_code}&count=1'

# 更新请求头
headers = {
    'Cookie': config['headers']['cookie'],
    'User-Agent': config['headers']['user_agent'],
    'Referer': f'https://xueqiu.com/P/{portfolio_code}',
    'Accept': 'application/json, text/plain, */*'
}

# 发送消息到 Telegram 并返回消息 ID
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
    data = {
        'chat_id': telegram_chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=data)
    print(Fore.BLUE + f"Telegram 发送消息响应：{response.text}")

    if response.status_code == 200:
        response_json = response.json()
        if 'result' in response_json and 'message_id' in response_json['result']:
            message_id = response_json['result']['message_id']
            print(Fore.GREEN + "消息已发送到 Telegram")
            return message_id
        else:
            print(Fore.RED + f"响应中缺少 message_id：{response_json}")
            return None
    else:
        print(Fore.RED + f"发送消息失败，错误代码：{response.status_code}")
        return None

# 将消息置顶
def pin_telegram_message(message_id):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/pinChatMessage'
    data = {
        'chat_id': telegram_chat_id,
        'message_id': message_id
    }
    response = requests.post(url, data=data)
    print(Fore.BLUE + f"Telegram 置顶消息响应：{response.text}")

    if response.status_code == 200:
        print(Fore.GREEN + "消息已置顶")
    else:
        print(Fore.RED + f"置顶消息失败，错误代码：{response.status_code}")

# 将时间戳转换为可读的日期时间格式
def format_timestamp(timestamp):
    dt = datetime.fromtimestamp(timestamp / 1000)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# 构建调仓信息消息
def build_message(rebalancing):
    updated_at = format_timestamp(rebalancing['updated_at'])
    message = "*雪球组合调仓通知*\n\n"
    message += f"调仓时间：{updated_at}\n"
    message += "调仓详情如下：\n"
    for stock in rebalancing['rebalancing_histories']:
        message += f"股票：{stock['stock_name']} ({stock['stock_symbol']})\n"
        message += f"操作：{'买入' if stock['target_weight'] > 0 else '卖出'}\n"
        message += f"目标权重：{stock['target_weight']}%\n\n"
    return message

# 记录组合的上一次调仓信息
last_rebalancing_id = None

# 循环检测调仓变化
while True:
    try:
        response = requests.get(xueqiu_api_url, headers=headers)
        if response.status_code != 200:
            print(Fore.RED + f"请求错误：{response.status_code}，响应信息：{response.text}")
            time.sleep(60)
            continue

        data = response.json()
        if data['list']:
            latest_rebalancing = data['list'][0]
            latest_rebalancing_id = latest_rebalancing['id']

            if last_rebalancing_id is None:
                last_rebalancing_id = latest_rebalancing_id
                print(Fore.YELLOW + "初始化调仓 ID 并发送最新调仓信息")
                message = build_message(latest_rebalancing)
                message_id = send_telegram_message(message)
                if message_id:
                    pin_telegram_message(message_id)

            elif latest_rebalancing_id != last_rebalancing_id:
                last_rebalancing_id = latest_rebalancing_id
                print(Fore.CYAN + f"检测到新调仓：{latest_rebalancing_id}")
                message = build_message(latest_rebalancing)
                message_id = send_telegram_message(message)
                if message_id:
                    pin_telegram_message(message_id)

        else:
            print(Fore.YELLOW + "没有新的调仓信息")

        time.sleep(60)

    except Exception as e:
        print(Fore.RED + f"出现错误：{e}")
        time.sleep(60)
