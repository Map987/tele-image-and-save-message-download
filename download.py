import json
from telethon import TelegramClient, events
import socks
import os
from telethon.tl.functions.messages import GetHistoryRequest
from telethon import TelegramClient, events, functions, types


# 设置 TelegramClient，连接到 Telegram API
client = TelegramClient(
    'demo',
    '换api_id',
    '换api_hash'
)

async def download_media(message, path):
    """
    下载消息中的媒体文件。

    参数:
    message -- Telegram消息对象
    path -- 保存文件的目录
    """
    if message.media:
        file = await client.download_media(message, file=path)
        return file
    return None

async def fetch_messages(channel_username, download_path):
    """
    获取指定频道的所有消息，并下载其中的媒体文件。

    参数:
    channel_username -- 目标频道的用户名
    download_path -- 下载文件的保存目录
    """
    channel_entity = await client.get_input_entity(channel_username)
    offset_id = 0  # 初始消息 ID 偏移量
    limit = 100  # 设置获取消息的数量上限

    while True:
        # 请求消息记录
        history = await client(functions.messages.GetHistoryRequest(
            peer=channel_entity,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=100,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:  # 当没有更多消息时结束循环
            break

        for message in history.messages:
            # 下载媒体文件
            file_path = await download_media(message, download_path)
            if file_path:
                print(f"Downloaded file: {file_path}")

        offset_id = history.messages[-1].id
        print(f"Fetched messages: {offset_id}")
    return

async def main():
    """
    主程序：从指定频道获取消息并下载媒体文件。
    """
    await client.start()  # 启动 Telegram 客户端
    print("Client Created")

    channel_username = 'me'  # 你要抓取的 Telegram 频道用户名
    download_path = '/storage/emulated/0/121212/1/'  # 保存下载文件的目录

    # 创建下载目录
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # 获取消息并下载媒体文件
    await fetch_messages(channel_username, download_path)

    await client.disconnect()  # 断开 Telegram 客户端连接

# 当该脚本作为主程序运行时
if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
