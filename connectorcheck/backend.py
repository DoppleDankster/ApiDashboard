from typing import Sequence, Dict, List, Optional
from datetime import date, timedelta, datetime
from requests import get
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError, ConnectionError
from furl import furl
from .dataclass import DataProvider, Instrument


class Backend:
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
    ):

        """
        A Small interface to a Django API.

        Args:
            base_url(str): The domain ex `demo.datapred.com`
            username(str): The login name
            password(str): The login password
            date_filter(str): A `start_date` filter for some queries
        """
        self.base_url = furl(base_url)
        self.auth = HTTPBasicAuth(username=username, password=password)
        self.date_filter = self.generate_date_filter()

    def get_data_providers(self) -> Sequence[DataProvider]:
        """
        Get the list of data-providers from the api.

        Returns:
            []DataProviders: The list of DataProviders
        """
        return_list = []

        endpoint = "/procurement/data-providers/"
        params = {"format": "json"}
        url = self.generate_url(endpoint=endpoint, params=params)
        response = self.generate_request(url=url).json()
        providers = response["results"]
        for provider in providers:
            id = provider["id"]
            instruments = self.get_intruments(id)
            return_list.append(
                DataProvider(**provider, instruments=instruments)
            )
        return return_list

    def get_intruments(self, data_provider_id: int) -> Sequence[Instrument]:
        """
        Get the list of instrument from a given data provider.

        Args:
            data_provider_id(int): The id of the data provider

        Returns:
            []Instruments : An array of Instruments
        """
        return_list = []
        endpoint = (
            f"/procurement/data-providers/{data_provider_id}/instruments/"
        )
        params = {"format": "json"}
        url = self.generate_url(endpoint=endpoint, params=params)
        response = self.generate_request(url=url).json()
        for instrument in response["results"]:
            instrument_id = instrument["id"]
            last_raw_data = self.get_instrument_last_raw_data(
                data_provider_id, instrument_id
            )
            return_list.append(
                Instrument(**instrument, last_raw_data=last_raw_data)
            )
        return return_list

    def get_instrument_last_raw_data(
        self, data_provider_id: int, instrument_id: int
    ) -> Optional[Dict]:
        """
        Get the latest raw data from an instrument

        Args:
            data_provider_id(int): The id of the data provider
            intrument_ud(int): The id of the instrument

        Returns:
            (dict): The latest raw_data entry
        """
        endpoint = (
            f"/procurement/data-providers/{data_provider_id}"
            f"/instruments/{instrument_id}/data"
        )
        params = {
            "format": "json",
            "start_date": self.date_filter,
            "min_samples": "-1",
        }
        url = self.generate_url(endpoint=endpoint, params=params)
        response = self.generate_request(url=url).json()
        if len(response) > 0:
            return response[-1]
        return None

    def generate_url(self, endpoint: str, params: dict) -> furl:
        """
        Generate a sanitized url from a base, a path and some query params.

        Args:
            base_url: The domain ex: https://api.demo.datapred.com
            endpoint: The path of the endpoint ex: `/procurement/data-providers/`
            params: The query params in key/value pairs ex {"format":"json"}

        Returns:
            (str): The complete url
        """
        url = self.base_url / endpoint
        url.args = params
        return url

    def generate_request(self, url: furl):
        """
        Run a get request with authentication

        Args:
            url(furl): The complete URL with it's query params

        Returns:
            Response Object

        Throws:
            BackendError
        """
        try:
            response = get(url=url, auth=self.auth)
            response.raise_for_status()
            return response
        except (HTTPError, ConnectionError):
            raise BackendError(
                host=url.host,
                endpoint=url.path,
                status_code=response.status_code,
                message=response.text,
            )

    @staticmethod
    def generate_date_filter():
        today = date.today()
        yesterday = today - timedelta(days=1)
        return yesterday


class BackendError(Exception):
    def __init__(self, message, host, endpoint, status_code):
        super().__init__(message)
        self.host = host
        self.endpoint = endpoint
        self.status_code = status_code
