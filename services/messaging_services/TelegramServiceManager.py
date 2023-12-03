import asyncio
import telegram

from services.messaging_services.messaging_interface import MessagingInterface


class TelegramSender(MessagingInterface):
    def __init__(self, token):
        print(f"Service Manager for Telegram initialized with token {token}")
        self.bot = telegram.Bot(token=token)

    def send(self, chat_id, message):
        asyncio.run(self.bot.send_message(chat_id=chat_id, text=message))
