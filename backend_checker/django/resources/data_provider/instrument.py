#!/usr/bin/env python3

from typing import List, Dict
from datetime import datetime
from backend_checker.django.resources import Resource
from backend_checker.services.backend import Backend
from . import DataProvider


class Instrument(Resource):
    def __init__(
        self,
        backend: Backend,
        data_provider: DataProvider,
        instrument_id: int,
        id_at_provider: str,
        instrument_fields: List[str],
    ):
        self.backend = backend
        self.data_provider = data_provider
        self._id = instrument_id
        self.id_at_provider = id_at_provider
        self.instrument_fields = instrument_fields
        self.raw_data = None

    def load(self, date_filter: datetime) -> None:
        """
        Get the raw_data from the instrument as a JSON array.


        Sets the return value of the query as the self.raw_data
        attribute.

        Params:
            date_filter(datetime): start_date for the query

        Returns:
            None
        """

        self.raw_data = self.backend.get_instrument_raw_data(
            self.data_provider._id, self._id, date_filter.isoformat()
        )
