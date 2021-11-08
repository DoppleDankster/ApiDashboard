#!/usr/bin/env python3

from typing import Sequence, Dict
from requests import get
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError, ConnectionError
from furl import furl


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

    def get_data_providers(self) -> Sequence[Dict]:
        """
        Return the list of data providers as a JSON array.
        """

        endpoint = "/procurement/data-providers/"
        params = {"format": "json"}
        url = self.generate_url(endpoint=endpoint, params=params)
        response = self.generate_request(url=url).json()
        return response["results"]

    def get_data_provider(self, provider_id: int) -> Dict:
        """
        Return a data provider in JSON format
        """
        endpoint = f"/procurement/data-providers/{provider_id}/"
        params = {"format": "json"}
        url = self.generate_url(endpoint=endpoint, params=params)
        return self.generate_request(url=url).json()

    def get_data_provider_instruments(
        self, provider_id: int
    ) -> Sequence[Dict]:
        """
        Return the list of instruments from a data provider as a JSON array
        """
        endpoint = f"/procurement/data-providers/{provider_id}/instruments/"
        params = {"format": "json"}
        url = self.generate_url(endpoint=endpoint, params=params)
        response = self.generate_request(url=url).json()
        return response["results"]

    def get_instrument(self, provider_id: int, instrument_id: int) -> Dict:
        """
        Return a data provider instrument in JSON format
        """
        endpoint = f"/procurement/data-providers/{provider_id}/instruments/{instrument_id}"
        params = {"format": "json"}
        url = self.generate_url(endpoint=endpoint, params=params)
        return self.generate_request(url=url).json()

    def get_instrument_raw_data(
        self, provider_id: int, instrument_id: int, start_date: str
    ) -> Sequence[Dict]:
        """
        Return the raw data from an instrument as a JSON array
        """

        endpoint = (
            f"/procurement/data-providers/{provider_id}"
            f"/instruments/{instrument_id}/data"
        )
        params = {
            "format": "json",
            "start_date": start_date,
            "min_samples": "-1",
        }
        url = self.generate_url(endpoint=endpoint, params=params)
        response = self.generate_request(url=url).json()
        return response["results"]

    def get_flows(self) -> Sequence[Dict]:
        """
        Return the list of flows as a JSON array.
        """
        endpoint = "/procurement/flows/"
        params = {"format": "json"}
        url = self.generate_url(endpoint=endpoint, params=params)
        response = self.generate_request(url=url).json()
        return response["results"]

    def get_flow(self, flow_id: int) -> Dict:
        """
        Return a flow in JSON format
        """
        endpoint = f"/procurement/flows/{flow_id}/"
        params = {"format": "json"}
        url = self.generate_url(endpoint=endpoint, params=params)
        return self.generate_request(url=url).json()

    def get_commodities(self) -> Sequence[Dict]:
        """
        Return the list of commodities as a JSON array.
        """
        endpoint = "/procurement/commodities/"
        params = {"format": "json"}
        url = self.generate_url(endpoint=endpoint, params=params)
        response = self.generate_request(url=url).json()
        return response["results"]

    def get_commodity(self, commodity_id: int) -> Dict:
        """
        Return a commodity in JSON format
        """
        endpoint = f"/procurement/commodities/{commodity_id}/"
        params = {"format": "json"}
        url = self.generate_url(endpoint=endpoint, params=params)
        response = self.generate_request(url=url).json()
        return response["results"]

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


class BackendError(Exception):
    def __init__(self, message, host, endpoint, status_code):
        super().__init__(message)
        self.host = host
        self.endpoint = endpoint
        self.status_code = status_code
