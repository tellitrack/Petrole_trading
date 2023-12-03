import pandas as pd
from enum import Enum
from _api_manager.rest_service_manager import ClientApp, ServiceManager

# TODO create a cool dataframe for each method

# API documentation: https://www.alphavantage.co/documentation/

_URL = 'https://www.alphavantage.co/'


class AlphaVantage(Enum):
    TIME_SERIES_INTRADAY = 'query?function=TIME_SERIES_INTRADAY'
    TIME_SERIES_DAILY = 'query?function=TIME_SERIES_DAILY'
    TIME_SERIES_WEEKLY = 'query?function=TIME_SERIES_WEEKLY'
    TIME_SERIES_MONTHLY = 'query?function=TIME_SERIES_MONTHLY'
    SYMBOL_SEARCH = 'query?function=SYMBOL_SEARCH'


class AlphaVantageServiceManager:

    def __init__(self, client_id, client_secret, environnement):
        """
        :type client_id: str
        :param client_id: the client id of your client app
        :param client_secret: the client secret of your client app
        :param environnement: the environnement of your client app, supported values are: PROD, DEV, TEST
        """
        self.client_app = ClientApp(client_id=client_id,
                                    client_secret=client_secret,
                                    environnement=environnement)

        self.service_manager = ServiceManager(client_app=self.client_app,
                                              api_name="AlphaVantage")

    ####################################################################################################################
    #                                               TIME SERIES                                                        #
    ####################################################################################################################
    def get_time_series_intraday(self,
                                 symbol: str,
                                 interval: str,
                                 output_size: str = 'compact',
                                 datatype: str = 'json',
                                 response_as_dataframe: bool = False):
        uri = f'{_URL}'
        uri_endpoint = f'{AlphaVantage.TIME_SERIES_INTRADAY.value}'

        params = f'symbol={symbol}&'
        params += f'interval={interval}&'
        params += f'outputsize={output_size}&'
        params += f'datatype={datatype}&'
        params += f'apikey={self.client_app.client_id}'

        uri_request = f'{uri}{uri_endpoint}&{params}'
        response = self.service_manager.get(uri_request=uri_request)
        if response_as_dataframe:
            return pd.DataFrame(response)
        return response

    def get_time_series_daily(self,
                              symbol: str,
                              output_size: str = 'compact',
                              datatype: str = 'json',
                              response_as_dataframe: bool = False):
        uri = f'{_URL}'
        uri_endpoint = f'{AlphaVantage.TIME_SERIES_DAILY.value}'

        params = f'symbol={symbol}&'
        params += f'outputsize={output_size}&'
        params += f'datatype={datatype}&'
        params += f'apikey={self.client_app.client_id}'

        uri_request = f'{uri}{uri_endpoint}&{params}'
        response = self.service_manager.get(uri_request=uri_request)
        if response_as_dataframe:
            return pd.DataFrame(response)
        return response

    def get_time_series_weekly(self,
                               symbol: str,
                               datatype: str = 'json',
                               response_as_dataframe: bool = False):
        uri = f'{_URL}'
        uri_endpoint = f'{AlphaVantage.TIME_SERIES_WEEKLY.value}'

        params = f'symbol={symbol}&'
        params += f'datatype={datatype}&'
        params += f'apikey={self.client_app.client_id}'

        uri_request = f'{uri}{uri_endpoint}&{params}'
        response = self.service_manager.get(uri_request=uri_request)
        if response_as_dataframe:
            return pd.DataFrame(response)
        return response

    def get_time_series_monthly(self,
                                symbol: str,
                                datatype: str = 'json',
                                response_as_dataframe: bool = False):
        uri = f'{_URL}'
        uri_endpoint = f'{AlphaVantage.TIME_SERIES_MONTHLY.value}'

        params = f'symbol={symbol}&'
        params += f'datatype={datatype}&'
        params += f'apikey={self.client_app.client_id}'

        uri_request = f'{uri}{uri_endpoint}&{params}'
        response = self.service_manager.get(uri_request=uri_request)
        if response_as_dataframe:
            return pd.DataFrame(response)
        return response

    ####################################################################################################################
    #                                               SYMBOL                                                             #
    ####################################################################################################################

    def get_symbol_search(self,
                          keywords: str,
                          datatype: str = 'json',
                          response_as_dataframe: bool = False):
        uri = f'{_URL}'
        uri_endpoint = f'{AlphaVantage.SYMBOL_SEARCH.value}'

        params = f'keywords={keywords}&'
        params += f'datatype={datatype}&'
        params += f'apikey={self.client_app.client_id}'

        uri_request = f'{uri}{uri_endpoint}&{params}'
        response = self.service_manager.get(uri_request=uri_request)
        if response_as_dataframe:
            return pd.DataFrame(response)
        return response
