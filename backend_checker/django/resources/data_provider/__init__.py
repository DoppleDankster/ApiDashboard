#!/usr/bin/env python3

from backend_checker.django.resources import Resource
from backend_checker.services.backend import Backend


class DataProvider(Resource):
    def __init__(
        self, backend: Backend, provider_id: int, name: str, description: str
    ):
        self.backend = backend
        self._id = provider_id
        self.name = name
        self.description = description
        self.instruments = None

    def load_instruments(self) -> None:
        """
        Get the list of instrument of the DataProvider

        Sets the result of the query as the self.instruments
        attribute.

        Returns:
            None
        """

        self.instruments = self.backend.get_data_provider_instruments(
            provider_id=self._id
        )
