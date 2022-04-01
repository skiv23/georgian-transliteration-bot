# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List

from telebot.async_telebot import AsyncTeleBot


@dataclass
class Transliterate:
    chat_id: int
    bot: AsyncTeleBot
    messages: List[str] = field(default_factory=list)
    initial_message: str = ""
    characters: str = ""
    mapping = {
        "ა": "а", "ბ": "б", "გ": "г", "დ": "д", "ე": "е", "ვ": "в", "ზ": "з", "თ": "т",
        "ი": "и", "უ": "у", "კ": "к", "ლ": "л", "მ": "м", "ნ": "н", "ო": "о", "პ": "п", "ჟ": "ж", "რ": "р",
        "ს": "с", "ტ": "т", "ფ": "п", "ქ": "к", "ღ": "р", "ყ": "кх", "შ": "ш", "ჩ": "ч", "ც": "ц", "ძ": "дз",
        "წ": "ц", "ჭ": "ч", "ხ": "х", "ჯ": "дж", "ჰ": "х"
    }

    async def add_message(self, message):
        text = message.text

        if not self.initial_message:
            self.initial_message = text.lower()  # Georgian language doesn't have letter case
            await self.bot.send_message(
                message.chat.id,
                f"Type in the characters you want to use",
            )

        elif not self.characters:
            self.characters = text

        if self.initial_message and self.characters:
            return await self.transliterate()
        return False

    async def get_characters_list(self):
        if self.characters == 'all':
            return self.mapping.keys()
        return list(self.characters)

    async def transliterate(self):
        try:
            characters_list = await self.get_characters_list()
            replaced_chars = []
            non_replaced_messages = []
            for char in characters_list:
                if self.mapping[char] in replaced_chars:
                    non_replaced_messages.append(
                        f"{self.mapping[char]} was already replaced, transliteration was not applied for {char}"
                    )
                else:
                    self.initial_message = self.initial_message.replace(self.mapping[char], char)
                    replaced_chars.append(self.mapping[char])
            if non_replaced_messages:
                await self.bot.send_message(
                    self.chat_id,
                    '\n'.join(non_replaced_messages),
                )
            await self.bot.send_message(
                self.chat_id,
                self.initial_message,
            )
        except KeyError:
            await self.bot.send_message(
                self.chat_id,
                "Something went wrong, check your message or characters",
            )
        return True
