import os
import yaml
from enum import Enum


class CredentialKey(str, Enum):
    ALPHA_VANTAGE = 'ALPHA_VANTAGE'
    WEALTH_SIMPLE = 'WEALTH_SIMPLE'
    ALPACA_LIVE = 'ALPACA_LIVE'
    ALPACA_PAPER = 'ALPACA_PAPER'
    TELEGRAM = 'TELEGRAM'
    EIA = 'EIA'


class CredentialsManager:
    def __init__(self, credentials_file):
        with open(credentials_file, 'r') as file:
            self.credentials = yaml.safe_load(file)

    def get_credentials(self, key: CredentialKey):
        if key == CredentialKey.WEALTH_SIMPLE:
            return self._get_wealth_simple_credentials()
        elif key == CredentialKey.ALPACA_LIVE:
            return self._get_alpaca_credentials('LIVE')
        elif key == CredentialKey.ALPACA_PAPER:
            return self._get_alpaca_credentials('PAPER')
        elif key == CredentialKey.TELEGRAM:
            return self._get_telegram_credentials()
        elif key == CredentialKey.EIA:
            return self._get_eia_credentials()
        elif key == CredentialKey.ALPHA_VANTAGE:
            return self._get_alpha_vantage_credentials()
        else:
            raise ValueError(f"Unsupported credential key: {key}")

    def _get_wealth_simple_credentials(self):
        credentials = self.credentials.get('WEALTH_SIMPLE', {})
        url = credentials.get('URL')
        username = os.getenv(credentials.get('USERNAME'))
        password = os.getenv(credentials.get('PASSWORD'))
        recovery_code = credentials.get('RECOVERY_CODE')
        return url, username, password, recovery_code

    def _get_alpaca_credentials(self, account_type):
        credentials = self.credentials.get('ALPACA', {}).get(account_type, {})
        api_key = os.getenv(credentials.get('API_KEY'))
        api_secret = os.getenv(credentials.get('API_SECRET'))
        return api_key, api_secret

    def _get_telegram_credentials(self):
        credentials = self.credentials.get('TELEGRAM', {})
        token = os.getenv(credentials.get('TOKEN'))
        chat_ids = {k: os.getenv(v) for k, v in credentials.get('CHAT_IDS', {}).items()}
        return token, chat_ids

    def _get_eia_credentials(self):
        credentials = self.credentials.get('EIA', {})
        api_key = os.getenv(credentials.get('API_KEY'))
        return api_key

    def _get_alpha_vantage_credentials(self):
        credentials = self.credentials.get('ALPHA_VANTAGE', {})
        api_key = os.getenv(credentials.get('API_KEY'))
        return api_key
