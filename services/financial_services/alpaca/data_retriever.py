from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca_trade_api.rest import REST

# PAPER TRADING
API_KEY = "PKK7IPPJ5OTJ7QR5XGSW"
API_SECRET = "anhIPRhvNer0z4ZVxO3pd1tBXHCd81zXmw4VxbB6"


client_crypto = CryptoHistoricalDataClient()
client_stock = StockHistoricalDataClient(
    api_key="AKED28NA21OAN4WW3BVB",
    secret_key="zQ1ZEPcc2YyRcIchpR07ws52qMUPmJLMEBbV6qAX",
)


request_params_crypto = CryptoBarsRequest(
    symbol_or_symbols=["BTC/USD"],
    timeframe=TimeFrame.Day,
    start="2022-09-01T00:00:00",  # Added time component
    end="2022-09-07T23:59:59"  # Added time component
)

request_param_stocks = StockBarsRequest(
    symbol_or_symbols=["USL"],
    timeframe=TimeFrame.Day,
    start="2016-01-01T00:00:00",  # Added time component
    end="2023-11-24T23:59:59"  # Added time component
)

# btc_bars = client_crypto.get_crypto_bars(request_params_crypto)
# dataf = btc_bars.df

bars = client_stock.get_stock_bars(request_param_stocks)

dataf = bars.df
dataf.to_csv("USL_DAY_from_2016-01-01_to_2023-11-24.csv", index=True)
print(1)
