from _helpers.dates import to_date
from _helpers.iterables import iterable


@iterable
class Quote:
    def __init__(self, app_name, app_object, infos):
        self.app_name = app_name
        if app_name == "WealthSimple":
            self._process_wealthsimple_data(app_object)
        elif app_name == "YahooFinance":
            self._process_yahoofinance_data(app_object, infos)
        else:
            raise ValueError(f"Nom d'application non pris en charge : {app_name}")

    def _process_wealthsimple_data(self, app_object):
        self.security_id = Security(identifier=app_object.security_id).ticker
        self.timestamp = to_date(app_object.date, 'WealthSimple')
        self.close = app_object.close
        self.price = app_object.adjusted_price
        self.volume = None

    def _process_yahoofinance_data(self, app_object, infos):
        app_object['ticker'] = infos['ticker']
        app_object['interval'] = infos['interval']
        app_object.index.name = 'timestamp'
        self.reworked_df = app_object
