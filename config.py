"""
Centraliser toutes les configurations globales, y compris les chemins de fichiers, les paramètres de connexion aux API, etc.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CREDENTIALS_PATH = os.path.join(BASE_DIR, 'management', 'credentials', 'credentials.yml')
DATABASES_PETROLEUM_PATH = os.path.join(BASE_DIR, 'management', 'data', 'petroleum')
DATABASES_CRYPTO_PATH = os.path.join(BASE_DIR, 'management', 'data', 'crypto')

# TODO: amend all paths
MAIN_PATH = 'G:\\My Drive\\Investment'
OLD_MAIN_PATH = "C:\\Users\\hyacinthe\\Desktop"

ORDER_BOOK_PATH = MAIN_PATH + '\\databases\\OrderBook.csv'
POSITIONS_PATH = MAIN_PATH + '\\databases\\Positions.csv'
CASH_ACCOUNT_PATH = MAIN_PATH + '\\databases\\CashAccount.csv'
PNL_PATH = MAIN_PATH + '\\databases\\PnL.csv'
SECURITIES_PATH = MAIN_PATH + '\\databases\\Securities.csv'
QUOTES_PATH = MAIN_PATH + '\\databases\\Quotes\\'
STRATEGIES_PATH = MAIN_PATH + '\\databases\\Strategies\\'

RESULTS_PROD_PATH = MAIN_PATH + '\\strategies\\prod\\'
RESULTS_BACKTEST_PATH = MAIN_PATH + '\\strategies\\backtest\\results\\'
RESULTS_STUDIES_PATH = MAIN_PATH + '\\strategies\\studies\\results\\'
RESULTS_UAT_PATH = MAIN_PATH + '\\strategies\\uat\\results\\'

TO_BOOK_PATH = MAIN_PATH + '\\strategies\\prod\\'
TOKENS = MAIN_PATH + '\\databases\\tokens.json'
