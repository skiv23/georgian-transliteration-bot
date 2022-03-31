# -*- coding: utf-8 -*-
import asyncio
import os

from telebot import async_telebot, types

from transliterate import Transliterate

bot = async_telebot.AsyncTeleBot(os.environ["TOKEN"], parse_mode=None)

chats = {}


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(
        message,
        "Hello. This bot allows you to transliterate russian text into Georgian letters. "
        "Type /transliterate to start or /help to see the list of available characters"
    )


@bot.message_handler(commands=['help'])
async def send_welcome(message):
    await bot.reply_to(
        message,
        "Here's the list of available characters: а=ა б=ბ г=გ д=დ е=ე  в=ვ з=ზ т(ь)=თ и=ი у=უ к=კ л=ლ м=მ н=ნ о=ო "
        "п=პ ж=ჟ р= რ с=ს т=ტ пь=ფ кь=ქ гъ=ღ кх=ყ ш=შ ч=ჩ ц=ც дз=ძ цъ=წ чъ=ჭ х=ხ дж=ჯ h(хь)=ჰ"
    )


@bot.message_handler(commands=['transliterate'])
async def transliterate(message):
    chat_id = message.chat.id
    chats[chat_id] = Transliterate(message.chat.id, bot)
    await bot.reply_to(message, "Paste in the text you want to transliterate")


@bot.message_handler(func=lambda message: True)
async def accept_message(message):
    chat_id = message.chat.id
    if chat_id in chats:
        if message.text in ['stop', '/stop']:
            del chats[chat_id]
        result = await chats[chat_id].add_message(message)
        if result:
            del chats[chat_id]


asyncio.run(bot.polling())
