import asyncio
import telegram

from config import CREDENTIALS_PATH
from messaging_interface import MessagingInterface
from management.credentials.credentials_manager import CredentialKey, CredentialsManager


class TelegramSender(MessagingInterface):
    def __init__(self, token):
        self.bot = telegram.Bot(token=token)

    def send(self, chat_id, message):
        asyncio.run(self.bot.send_message(chat_id=chat_id, text=message))


if __name__ == '__main__':
    credentials_manager = CredentialsManager(CREDENTIALS_PATH)
    telegram_token, telegram_chat_ids = credentials_manager.get_credentials(CredentialKey.TELEGRAM)
    group_chat_id = telegram_chat_ids.get('TRADING_SIGNALS')
    telegram_sender = TelegramSender(token=telegram_token)
    telegram_sender.send(chat_id=group_chat_id, message="Test message")
