import pandas as pd
from enum import Enum
from typing import List, Dict

from _api_manager.rest_service_manager import ClientApp, ServiceManager

_URL = 'https://api.eia.gov/v2/'


class EIA(Enum):
    PETROLEUM_STOCKS = 'petroleum/stoc/wstk'
    PETROLEUM_PRICES = 'petroleum/prices'
    PETROLEUM_PRODUCTION = 'petroleum/production'
    PETROLEUM_IMPORTS = 'petroleum/imports'
    PETROLEUM_EXPORTS = 'petroleum/exports'
    PETROLEUM_CONSUMPTION = 'petroleum/consumption'
    PETROLEUM_INVENTORIES = 'petroleum/inventories'
    PETROLEUM_SUPPLIES = 'petroleum/supplies'
    PETROLEUM_DEMAND = 'petroleum/demand'


class EIAServiceManager:

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
                                              api_name="EIA")

    def get_petroleum_stocks(self,
                             frequency: str,
                             data: str,
                             start: str,
                             end: str,
                             sort: List[Dict[str, str]],
                             offset: int,
                             length: int,
                             area_name_filter: str = '',
                             series_filter: str = '',
                             response_as_dataframe: bool = True):
        uri = f'{_URL}'
        uri_endpoint = f'{EIA.PETROLEUM_STOCKS.value}'

        params = f'/data/?api_key={self.client_app.client_id}&'
        params += f'frequency={frequency}&'
        params += f'data[0]={data}&'
        params += f'start={start}&'
        params += f'end={end}&'
        params += f'sort[0][column]={sort[0]["column"]}&'
        params += f'sort[0][direction]={sort[0]["direction"]}&'
        params += f'offset={offset}&'
        params += f'length={length}'

        uri_request = f'{uri}{uri_endpoint}{params}'
        response = self.service_manager.get(uri_request=uri_request)
        response_dataf = pd.DataFrame(response['response']['data'])
        if area_name_filter:
            response_dataf = response_dataf[response_dataf['area-name'] == area_name_filter]
        if series_filter:
            response_dataf = response_dataf[response_dataf['series'] == series_filter][['period', 'value']]
        response_dataf = response_dataf.reset_index(drop=True)
        return response_dataf if response_as_dataframe else response
