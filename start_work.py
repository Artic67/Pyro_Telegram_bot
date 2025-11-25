import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client
from decouple import config

API_ID = config('API_ID')
API_HASH = config('API_HASH')
PHONE = config('PHONE')
LOGIN = config('LOGIN')
HOSTNAME = config('PROXY_HOSTNAME')
PORT = config('PROXY_PORT', cast=int)
PROXY_USERNAME = config('PROXY_USERNAME')
PROXY_PASS = config('PROXY_PASS')

proxy = {
        "scheme": "socks5",
        "hostname": HOSTNAME,
        "port": PORT,
        "username": PROXY_USERNAME,
        "password": PROXY_PASS
    }



bot = Client(name=LOGIN, api_id=API_ID, api_hash=API_HASH, phone_number=PHONE, proxy=proxy)
bot.start()
bot.send_message(chat_id='me', text='Тестовое сообщение с отправкой себе')
bot.stop()