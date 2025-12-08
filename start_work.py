import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from decouple import config
from pyrogram.types import Message
from emoji import demojize
import json


API_ID = config('API_ID')
API_HASH = config('API_HASH')
PHONE = config('PHONE')
LOGIN = config('LOGIN')
HOSTNAME = config('PROXY_HOSTNAME')
PORT = config('PROXY_PORT', cast=int)
PROXY_USERNAME = config('PROXY_USERNAME')
PROXY_PASS = config('PROXY_PASS')
TG_ACC1 = config('telegram_acc1', cast=int)
TARGET_CHAT = config('target_chat', cast=int)

skipNumAds = 0

proxy = {
        "scheme": "socks5",
        "hostname": HOSTNAME,
        "port": PORT,
        "username": PROXY_USERNAME,
        "password": PROXY_PASS
    }

with open("banwordlist.json", mode="r", encoding="utf-8") as read_file:
    banwordList = json.load(read_file)["banwords"]


async def show_history():
    async with bot:
        # "me" refers to your own chat (Saved Messages)
        counter = 0
        async for message in bot.get_chat_history(TARGET_CHAT):
            if counter < 10:
                print(message)
                print(len(str(message.caption)))
                print(str(message.caption))
                counter += 1
            else:
                break

# Inbound message handler
async def echo_handler(client: Client, message: Message):
    try:

        global skipNumAds

        if skipNumAds > 0:
            skipNumAds -= 1
            return

        #print("Wait 1 sec")
        #await asyncio.sleep(4)

        #print(message)

        msgText = str(message.text)

        if '1. Налаштування анкети' in msgText:
            await client.send_message(chat_id=message.chat.id, text="🎫")
            
        elif getattr(message, "caption"):

            msgCaption = str(message.caption)
            print(demojize(msgCaption))

            if ": Александр\n" in msgCaption:
                print("alex detected")
                return
        
            if len(msgCaption) > 250:
                print("Max caption length exceded.")
                await client.send_message(chat_id=message.chat.id, text="❌")
                return

            for banword in banwordList:
                if banword in msgCaption.lower():
                    print(f"Banword detected: {banword}.")
                    await client.send_message(chat_id=message.chat.id, text="❌")
                    return

            print("Liked message")
            await client.send_message(chat_id=message.chat.id, text="💖")
            return


        elif "Вибір потрібно зробити" in msgText:
            await client.send_message(chat_id=message.chat.id, text="/profile")

        elif "Продовжуємо пошук?" in msgText:
            await client.send_message(chat_id=message.chat.id, text="Продовжити пошук")

        elif "Хтось лайкнув вашу анкету!" in msgText:
            print("Хтось лайкнув анкету")

        elif "Ви щойно отримали взаємний лайк" in msgText:

            skipNumAds += 1

            likeName = msgText.split("🎯")[1].strip()

            # Find related message
            nearMessageIds = [message.id+i for i in range(-6, 7)]
            nearMessages = await client.get_messages(chat_id=message.chat.id, message_ids=nearMessageIds)

            for el in nearMessages:
                if getattr(el, "photo") and getattr(el, "caption"):
                    caption = str(el.caption).split("Ім'я:")[1].split("\n")[0].strip()
                    if caption == likeName:
                        if getattr(el, "media_group_id"):
                            await client.copy_media_group(chat_id=TG_ACC1, from_chat_id=message.chat.id, message_id=el.id)
                        else:
                            await client.copy_message(chat_id=TG_ACC1, from_chat_id=message.chat.id, message_id=el.id)

                        await client.copy_message(chat_id=TG_ACC1, from_chat_id=message.chat.id, message_id=message.id)
            
        else:
            print("------------ ELSE SECTION ------------")
            print(demojize(str(message.text)))

        # Sending a reply to the same chat
        # await client.send_message(chat_id=message.chat.id, text='⚙️')
        # await message.reply(text=f'{message.chat.id}')

    except Exception as error:
            print(error)


async def main():

    bot = Client(name=LOGIN, api_id=API_ID, api_hash=API_HASH, phone_number=PHONE, proxy=proxy)

    # Set up handlers
    bot.add_handler(MessageHandler(echo_handler, filters.user(TARGET_CHAT)))
    
    await bot.start()
    
    # Script start function
    await bot.send_message(chat_id=TARGET_CHAT, text='/profile')

    await idle()
    await bot.stop()

# Client launch
if __name__ == "__main__":
    asyncio.run(main())