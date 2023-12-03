import yfinance as yf


class YahooFinanceServiceManager:
    def __init__(self, ticker: str, start_date: str = None, end_date: str = None, period: str = None):
        print(f"ServiceManager for Yahoo Finance initialized with ticker {ticker}")
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.period = period

        self.ticker_base = yf.Ticker(self.ticker)

    def get_stock_price(self):
        return self.ticker_base.history(period=self.period)

    def get_historical_data(self):
        return self.ticker_base.history(start=self.start_date, end=self.end_date)

    def get_dividends(self):
        return self.ticker_base.dividends

    def get_splits(self):
        return self.ticker_base.splits

    def get_company_info(self):
        return self.ticker_base.info

    def get_financials(self):
        return self.ticker_base.financials

    def get_quarterly_financials(self):
        return self.ticker_base.quarterly_financials

    def get_balance_sheet(self):
        return self.ticker_base.balance_sheet

    def get_quarterly_balance_sheet(self):
        return self.ticker_base.quarterly_balance_sheet

    def get_cashflow(self):
        return self.ticker_base.cashflow

    def get_quarterly_cashflow(self):
        return self.ticker_base.quarterly_cashflow
