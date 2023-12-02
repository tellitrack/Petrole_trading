import os
import yaml

from enum import Enum


class CredentialKey(str, Enum):
    WEALTH_SIMPLE = 'WEALTH_SIMPLE'
    ALPACA_TRADING_LIVE = 'ALPACA.TRADING.LIVE'
    ALPACA_TRADING_PAPER = 'ALPACA.TRADING.PAPER'
    ALPACA_MARKET_DATA = 'ALPACA.MARKET_DATA'
    TELEGRAM = 'TELEGRAM'
    EIA = 'EIA'


class CredentialsManager:
    def __init__(self, credentials_file):
        with open(credentials_file, 'r') as file:
            self.credentials = yaml.safe_load(file)

    def get_credentials(self, key):
        credentials = self.credentials.get(key, {})

        if key == 'WEALTH_SIMPLE':
            url = credentials.get('URL')
            username = os.getenv(credentials.get('USERNAME'))
            password = os.getenv(credentials.get('PASSWORD'))
            return url, username, password

        elif key.startswith('ALPACA'):
            api_key = os.getenv(credentials.get('API_KEY'))
            api_secret = os.getenv(credentials.get('API_SECRET'))
            url = credentials.get('URL', '')

            if 'MARKET_DATA' in key or 'TRADING' in key:
                alpaca_account_type = key.split('.')[-1]
                account_type_credentials = credentials.get(alpaca_account_type, {})
                api_key = os.getenv(account_type_credentials.get('API_KEY'))
                api_secret = os.getenv(account_type_credentials.get('API_SECRET'))
                url = account_type_credentials.get('URL', url)

            return url, api_key, api_secret

        elif key == 'TELEGRAM':
            token = os.getenv(credentials.get('TOKEN'))
            chat_ids = {k: os.getenv(v) for k, v in credentials.get('CHAT_IDS', {}).items()}
            return token, chat_ids

        elif key == 'EIA':
            url = credentials.get('URL')
            api_key = os.getenv(credentials.get('API_KEY'))
            return url, api_key

        else:
            # Future credential structures
            pass
