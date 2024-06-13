import json
from telethon import TelegramClient
import socks
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
# 设置 TelegramClient，连接到 Telegram API
client = TelegramClient(
    'demo',
    'api_', # api_ 换成具体
    'api_hash' # api_hash换成具体
)

async def export_to_json(filename, data):
    """
    将数据导出到 JSON 文件中。

    参数:
    filename -- 导出文件的名称
    data -- 要导出的字典列表
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def fetch_messages(channel_username):
    """
    获取指定频道的所有消息。

    参数:
    channel_username -- 目标频道的用户名
    """
    channel_entity = await client.get_input_entity(channel_username)
    offset_id = 0  # 初始消息 ID 偏移量
    all_messages = []  # 存储所有消息的列表
    limit = 100  # 设置获取消息的数量上限

    while len(all_messages) < limit:
        # 请求消息记录
        history = await client(GetHistoryRequest(
            peer=channel_entity,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=min(100, limit - len(all_messages)),  # 每次请求的消息数量，但不超过剩余需要获取的消息数量
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:  # 当没有更多消息时结束循环
            break

        for message in history.messages:
            sender = await client.get_entity(message.chat_id)
            sender_username = sender.username if sender else 'Unknown'
            message_dict = {
                'id': message.id,
                'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                'chat_id': message.from_id,
                'sender_username': sender_username
            }
            if message.message:
                message_dict['text'] = message.message
            if message.photo:
                # 获取照片信息
                photo = message.photo
                message_dict['photo'] = {
                    'file_id': photo.id,
                    'file_unique_id': photo.access_hash
                }
            
            all_messages.append(message_dict)

        offset_id = history.messages[-1].id
        print(f"Fetched messages: {len(all_messages)}")
    return all_messages

async def main():
    """
    主程序：从指定频道获取消息并保存到 JSON 文件中。
    """
    await client.start()  # 启动 Telegram 客户端
    print("Client Created")

    channel_username = 'me'  # 你要抓取的 Telegram 频道 / 用户名 / me为收藏
    all_messages = await fetch_messages(channel_username)  # 获取消息

    # 导出消息到 JSON 文件
    await export_to_json('channel_messages.json', all_messages)

# 当该脚本作为主程序运行时
if __name__ == '__main__':
    client.loop.run_until_complete(main())
