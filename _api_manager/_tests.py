from config import CREDENTIALS_PATH
from management.credentials.credentials_manager import CredentialsManager, CredentialKey
from services.messaging_services.TelegramServiceManager import TelegramSender
from services.financial_services.AlphaVantageServiceManager import AlphaVantageServiceManager
from services.financial_services.EIAServiceManager import EIAServiceManager
from services.financial_services.YahooFinanceServiceManager import YahooFinanceServiceManager
from services.financial_services.AlpacaServiceManager import AlpacaDataServiceManager

credentials_manager = CredentialsManager(CREDENTIALS_PATH)

#######################################################################################################################
#   TELEGRAM                                                                                                          #
#######################################################################################################################

telegram_token, telegram_chat_ids = credentials_manager.get_credentials(CredentialKey.TELEGRAM)
group_chat_id = telegram_chat_ids.get('TRADING_SIGNALS')


def test_connection_service():
    response = TelegramSender(token=telegram_token)
    assert response is not None


def test_send_message():
    response = TelegramSender(token=telegram_token)
    response.send(chat_id=group_chat_id, message="Test si API fonctionnelle")
    assert response is not None


#######################################################################################################################
#   ALPHA VANTAGE                                                                                                     #
#######################################################################################################################

api_key = credentials_manager.get_credentials(CredentialKey.ALPHA_VANTAGE)
av_service_manager = AlphaVantageServiceManager(client_id=api_key, client_secret='', environnement='PROD')


def test_get_time_series_intraday():
    response = av_service_manager.get_time_series_intraday(symbol='UCO', interval='1min')
    assert response is not None


def test_get_time_series_daily():
    response = av_service_manager.get_time_series_daily(symbol='UCO')
    assert response is not None


def test_get_time_series_weekly():
    response = av_service_manager.get_time_series_weekly(symbol='UCO')
    assert response is not None


def test_get_time_series_monthly():
    response = av_service_manager.get_time_series_monthly(symbol='UCO')
    assert response is not None


def test_get_symbol_search():
    response = av_service_manager.get_symbol_search(keywords='UCO')
    assert response is not None


#######################################################################################################################
#   ENERGY INFORMATION ADMINISTRATION (EIA)                                                                           #
#######################################################################################################################

api_key = credentials_manager.get_credentials(CredentialKey.EIA)
eia_service_manager = EIAServiceManager(client_id=api_key, client_secret='', environnement='PROD')


def test_get_petroleum_stocks():
    response = eia_service_manager.get_petroleum_stocks(frequency='weekly',
                                                        data='value',
                                                        start='2020-01-01',
                                                        end='2020-01-10',
                                                        sort=[{'column': 'period', 'direction': 'asc'}],
                                                        offset=0,
                                                        length=1000,
                                                        area_name_filter='',
                                                        series_filter='',
                                                        response_as_dataframe=True)
    assert response is not None


#######################################################################################################################
#   YAHOO FINANCE                                                                                                     #
#######################################################################################################################

yf_service_manager = YahooFinanceServiceManager(ticker='AAPL',
                                                start_date='2021-01-01',
                                                end_date='2021-01-10',
                                                period='1d')


def test_get_stock_price():
    response = yf_service_manager.get_stock_price()
    assert response is not None


def test_get_historical_data():
    response = yf_service_manager.get_historical_data()
    assert response is not None


def test_get_dividends():
    response = yf_service_manager.get_dividends()
    assert response is not None


def test_get_splits():
    response = yf_service_manager.get_splits()
    assert response is not None


def test_get_company_info():
    response = yf_service_manager.get_company_info()
    assert response is not None


def test_get_financials():
    response = yf_service_manager.get_financials()
    assert response is not None


def test_get_quarterly_financials():
    response = yf_service_manager.get_quarterly_financials()
    assert response is not None


def test_get_balance_sheet():
    response = yf_service_manager.get_balance_sheet()
    assert response is not None


def test_get_quarterly_balance_sheet():
    response = yf_service_manager.get_quarterly_balance_sheet()
    assert response is not None


def test_get_cashflow():
    response = yf_service_manager.get_cashflow()
    assert response is not None


def test_get_quarterly_cashflow():
    response = yf_service_manager.get_quarterly_cashflow()
    assert response is not None


#######################################################################################################################
#   ALPACA MARKET DATA                                                                                                #
#######################################################################################################################

client_id, client_secret = credentials_manager.get_credentials(CredentialKey.ALPACA_PAPER)
alpaca_historical_data_service_manager = AlpacaDataServiceManager(client_id, client_secret, 'PROD')


def test_get_news():
    response = alpaca_historical_data_service_manager.get_news(start='2021-01-01', end='2021-01-10',
                                                               symbols=['AAPL', 'TSLA'])
    assert response is not None


def test_get_stocks_historical_auctions():
    response = alpaca_historical_data_service_manager.get_stocks_historial_auctions(start='2021-01-01',
                                                                                    end='2021-01-10',
                                                                                    symbols=['AAPL', 'TSLA'])
    assert response is not None


def test_get_stocks_historical_quotes():
    response = alpaca_historical_data_service_manager.get_stocks_historical_quotes(start='2021-01-01',
                                                                                   end='2021-01-10',
                                                                                   symbol='USO')
    assert response is not None


def test_get_stocks_latest_bars():
    response = alpaca_historical_data_service_manager.get_stocks_latest_bars(symbols=['USO', 'TSLA'])
    assert response is not None


def test_get_stocks_latest_quotes():
    response = alpaca_historical_data_service_manager.get_stocks_latest_quotes(symbols=['USO', 'TSLA'])
    assert response is not None


def test_get_stocks_snapshots():
    response = alpaca_historical_data_service_manager.get_stocks_snapshots(symbols=['USO', 'TSLA'])
    assert response is not None


if __name__ == '__main__':
    # TELEGRAM
    test_connection_service()
    test_send_message()

    # ALPHA VANTAGE
    test_get_time_series_intraday()
    test_get_time_series_daily()
    test_get_time_series_weekly()
    test_get_time_series_monthly()
    test_get_symbol_search()

    # EIA
    test_get_petroleum_stocks()

    # YAHOO FINANCE
    test_get_stock_price()
    test_get_historical_data()
    test_get_dividends()
    test_get_splits()
    test_get_company_info()
    test_get_financials()
    test_get_quarterly_financials()
    test_get_balance_sheet()
    test_get_quarterly_balance_sheet()
    test_get_cashflow()
    test_get_quarterly_cashflow()

    # ALPACA MARKET DATA
    test_get_news()
    test_get_stocks_historical_auctions()
    test_get_stocks_historical_quotes()
    test_get_stocks_latest_bars()
    test_get_stocks_latest_quotes()
    test_get_stocks_snapshots()

