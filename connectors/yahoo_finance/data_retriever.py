import pandas as pd
import yfinance as yf


class YahooFinanceDataRetriever:
    def __init__(self, ticker):
        self.ticker = ticker
        self.ticker_basic_data = yf.Ticker(ticker)

    def get_security_infos_by_ticker(self):
        try:
            from _helpers.objects import partial_flat
            return partial_flat(obj=self.ticker_basic_data, subobj='info')
        except Exception as e:
            print(f"Erreur lors de la récupération des informations : {e}")
            return {}

    def get_intraday_quotes(self, interval):
        try:
            quotes = Quote(
                app_object=self.ticker_basic_data.history(interval=interval),
                app_name='YahooFinance',
                infos={'ticker': self.ticker, 'interval': interval}
            )
            return quotes.reworked_df
        except Exception as e:
            print(f"Erreur lors de la récupération des cotations intrajournalières : {e}")
            return pd.DataFrame()

    def get_daily_quotes(self, interval):
        try:
            quotes = Quote(
                app_object=self.ticker_basic_data.history(interval=interval, period='max'),
                app_name='YahooFinance',
                infos={'ticker': self.ticker, 'interval': interval}
            )
            return quotes.reworked_df
        except Exception as e:
            print(f"Erreur lors de la récupération des cotations quotidiennes : {e}")
            return pd.DataFrame()


if __name__ == '__main__':
    retriever = YahooFinanceDataRetriever("AAPL")
    security_info = retriever.get_security_infos_by_ticker()
    intraday_quotes = retriever.get_intraday_quotes("1m")
    daily_quotes = retriever.get_daily_quotes("1d")
    print()
