from enum import Enum

from _api_manager.rest_service_manager import ClientApp, ServiceManager
from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest


# API Market Data Documentation: 'https://docs.alpaca.markets/docs/about-market-data-api"
# Swagger Link : 'https://docs.alpaca.markets/reference/intro/my-requests'

class Alpaca(Enum):
    DATA_STOCKS = 'https://data.alpaca.markets/v2/stocks/'
    DATA_NEWS = 'https://data.alpaca.markets/v1beta1/news'
    DATA_CRYPTOS = 'https://data.alpaca.markets/v1beta3/crypto/'


class AlpacaDataServiceManager:

    def __init__(self, client_id: str, client_secret: str, environnement):
        """
        Initialise le gestionnaire de service historique Alpaca.

        :param client_id: Identifiant client de l'application cliente.
        :param client_secret: Secret client de l'application cliente.
        :raises ValueError: Si udl_type n'est ni 'crypto' ni 'stock'.
        """

        print(f"ServiceManager for Alpaca Mkt Data initialized")

        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = {
            "accept": "application/json",
            "APCA-API-KEY-ID": self.client_id,
            "APCA-API-SECRET-KEY": self.client_secret
        }

        self.client_app = ClientApp(client_id, client_secret, environnement)
        self.service_manager = ServiceManager(client_app=self.client_app, api_name='Alpaca')

    ###################################################################################################################
    #   NEWS                                                                                                        #
    ###################################################################################################################

    def get_news(self, start: str, end: str, sort: str = 'desc', symbols: list = None, limit: int = 50,
                 include_content: bool = True, exclude_contentless: bool = True):
        """
        Récupère les dernières nouvelles.
        :param start: Date de début des nouvelles (exemple: '2023-01-03')
        :param end: Date de fin des nouvelles (exemple: '2023-12-01')
        :param sort: Ordre de tri des nouvelles (par défaut 'desc').
        :param symbols: Liste des symboles des instruments financiers.
        :param limit: Nombre maximum de nouvelles à retourner.
        :param include_content: Inclure le contenu des nouvelles.
        :param exclude_contentless: Exclure les nouvelles sans contenu.
        :return: Les dernières nouvelles.
        """

        uri = f"{Alpaca.DATA_NEWS.value}"

        params = f'?start={start}&end={end}&sort={sort}&limit={limit}'
        if symbols:
            symbols_str = "%2C".join(symbols)
            params += f"&symbols={symbols_str}"
        params += f'&include_content={include_content}&exclude_contentless={exclude_contentless}'

        uri_request = f"{uri}{params}"
        response = self.service_manager.get(uri_request=uri_request, headers=self.headers)
        return response

    ###################################################################################################################
    #   STOCKS                                                                                                        #
    ###################################################################################################################

    def get_stocks_historical_bars(self, request_params: StockBarsRequest):
        """
        Récupère les barres de données historiques pour les actions.

        :param request_params: Paramètres de la requête pour les données historiques.
        :return: Données historiques en fonction des paramètres de la requête.
        """
        self.service_manager = StockHistoricalDataClient(api_key=self.client_id, secret_key=self.client_secret)
        return self.service_manager.get_stock_bars(request_params)

    def get_stocks_historial_auctions(self, symbols: list, start: str, end: str, limit: int = 10000, feed: str = 'iex',
                                      currency: str = 'USD', sort: str = 'asc'):
        """
        Récupère les barres de données historiques pour les actions.

        :param symbols: Liste des symboles des instruments financiers.
        :param start: Date de début des données historiques (exemple: '2023-01-03T00:00:00Z')
        :param end: Date de fin des données historiques (exemple: '2023-12-01T00:00:00Z')
        :param limit: Nombre maximum de barres de données à retourner.
        :param feed: Source de données (par défaut 'iex')
                        'sip' pour toutes les bourses US, (besoin d'un abonnement payant)
                        'iex' pour la bourse Investors Exchange, (gratuit)
                        'otc' pour les bourses over the counter. (besoin d'un abonnement payant)
        :param currency: Devise des prix en format ISO 4217 (par défaut 'USD').
        :param sort: Ordre de tri des données historiques (par défaut 'asc').
        :return: Les barres de données historiques sous forme de texte.
        """

        symbols_str = ",".join(symbols)
        uri = f"{Alpaca.DATA_STOCKS.value}"
        uri_endpoint = f'auctions'
        params = f'?symbols={symbols_str}&start={start}&end={end}&limit={limit}&feed={feed}&currency={currency}&sort={sort}'
        uri_request = f"{uri}{uri_endpoint}{params}"
        response = self.service_manager.get(uri_request=uri_request, headers=self.headers)
        return response['auctions'] if response['auctions'] else response

    def get_stocks_historical_quotes(self, symbol: str, start: str, end: str, limit: int = 10000, feed: str = 'iex',
                                     currency: str = 'USD', sort: str = 'asc'):
        # symbols_str = "%2C".join(symbols)
        uri = f"{Alpaca.DATA_STOCKS.value}"
        uri_endpoint = f'quotes'
        params = f'?symbols={symbol}&start={start}&end={end}&limit={limit}&feed={feed}&currency={currency}&sort={sort}'
        uri_request = f"{uri}{uri_endpoint}{params}"
        response = self.service_manager.get(uri_request=uri_request, headers=self.headers)
        return response['quotes'] if response['quotes'] else response

    def get_stocks_latest_bars(self, symbols: list, currency: str = 'USD', feed: str = 'iex'):
        """
        Récupère les dernières barres de données historiques pour les symboles spécifiés.

        /!\ NE FONCTIONNE QUE POUR LES STOCKS

        :param symbols: Liste des symboles des instruments financiers.
        :param feed: Source de données (par défaut 'iex')
                        'sip' pour toutes les bourses US, (besoin d'un abonnement payant)
                        'iex' pour la bourse Investors Exchange, (gratuit)
                        'otc' pour les bourses over the counter. (besoin d'un abonnement payant)

        :param currency: Devise des prix en format ISO 4217 (par défaut 'USD').
        :return: Les dernières barres de données.
        """

        symbols_str = "%2C".join(symbols)
        uri = f"{Alpaca.DATA_STOCKS.value}"
        uri_endpoint = f'bars/latest'
        params = f'?symbols={symbols_str}&feed={feed}&currency={currency}'
        uri_request = f"{uri}{uri_endpoint}{params}"
        response = self.service_manager.get(uri_request=uri_request, headers=self.headers)
        return response['bars'] if response['bars'] else response

    def get_stocks_latest_quotes(self, symbols: list, currency: str = 'USD', feed: str = 'iex'):
        """
        Récupère les dernières barres de données historiques pour les symboles spécifiés.
        :param symbols: Liste des symboles des instruments financiers.
        :param feed: Source de données (par défaut 'iex')
                        'sip' pour toutes les bourses US, (besoin d'un abonnement payant)
                        'iex' pour la bourse Investors Exchange, (gratuit)
                        'otc' pour les bourses over the counter. (besoin d'un abonnement payant)
        :param currency: Devise des prix en format ISO 4217 (par défaut 'USD').
        :return: Les dernières quotes.
        """

        symbols_str = "%2C".join(symbols)
        uri = f"{Alpaca.DATA_STOCKS.value}"
        uri_endpoint = f'quotes/latest'
        params = f'?symbols={symbols_str}&feed={feed}&currency={currency}'
        uri_request = f"{uri}{uri_endpoint}{params}"
        response = self.service_manager.get(uri_request=uri_request, headers=self.headers)
        return response['quotes'] if response['quotes'] else response

    def get_stocks_snapshots(self, symbols: list, feed: str = 'iex', currency: str = 'USD'):
        """
        The snapshot endpoint for multiple tickers provides the latest trade, latest quote, minute bar daily bar,
        and previous daily bar data for each given ticker symbol.

        :param symbols: Liste des symboles des instruments financiers.
        :param feed: Source de données (par défaut 'iex')
                        'sip' pour toutes les bourses US, (besoin d'un abonnement payant)
                        'iex' pour la bourse Investors Exchange, (gratuit)
                        'otc' pour les bourses over the counter. (besoin d'un abonnement payant)
        :param currency: Devise des prix en format ISO 4217 (par défaut 'USD').
        """
        symbols_str = "%2C".join(symbols)
        uri = f"{Alpaca.DATA_STOCKS.value}"
        uri_endpoint = f'snapshots'
        params = f'?symbols={symbols_str}&feed={feed}&currency={currency}'
        uri_request = f"{uri}{uri_endpoint}{params}"
        response = self.service_manager.get(uri_request=uri_request, headers=self.headers)
        return response

    ###################################################################################################################
    #   CRYPTOS                                                                                                       #
    ###################################################################################################################

    def get_crypto_bars_request(self, request_params: CryptoBarsRequest):
        """
        Récupère les barres de données historiques pour les cryptomonnaies.
        :param request_params: Paramètres de la requête pour les données historiques.
        :return: Données historiques en fonction des paramètres de la requête.
        """

        self.service_manager = CryptoHistoricalDataClient()
        return self.service_manager.get_crypto_bars(request_params)
