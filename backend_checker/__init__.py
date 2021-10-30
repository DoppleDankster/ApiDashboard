__version__ = "0.1.0"
from typing import Dict, Optional, Sequence

from backend_checker.dataclass import DataProvider, Instrument
from .services.backend import Backend, BackendError
from .display import Displayer
from .services.slack import Slack


class BackendChecker:
    def __init__(
        self,
        backend: Backend,
        display: Optional[Displayer],
        slack: Optional[Slack],
    ):
        self.backend = backend
        self.display = display
        self.slack = slack

    def generate_data_providers(self):
        return self.backend.get_data_providers()

    def run(self):
        data_providers = self.generate_data_providers()
        if self.display:
            self.display.print_data_providers(data_providers)
        missing_data = self.check_for_missing_data(data_providers)
        if self.slack:
            message = self.generate_slack_report(missing_data)
            self.slack.send(message)

    @staticmethod
    def check_for_missing_data(
        data_providers: Sequence[DataProvider],
    ) -> Dict[str, Optional[Sequence[Instrument]]]:
        """
        Check for missing raw_data for each instrument.

        Each instrument is supposed to receive at least
        one new raw_data each day.

        This method returns the list of Instrument with missing data.

        Args:
            data_providers([]DataProvider): The list of data providers

        Returns:
            A dict with all the faulty Instrument sorted by provider
        """
        return_dict = {}
        for provider in data_providers:
            return_dict[provider.name] = []
            for instrument in provider.instruments:
                if not instrument.last_raw_data:
                    return_dict[provider.name].append(instrument)
        return return_dict

    def generate_slack_report(
        self,
        missing_data_dict: Dict,
    ):
        """
        Returns a Formatted Slack message.

        Args:
            missing_data_list: The list of faulty instruments.

        Returns:
            The formatted Slack Message
        """
        domain = self.backend.base_url
        if any(
            missing_data_dict[item] != [] for item in missing_data_dict.keys()
        ):
            return self.slack.generate_error_message(domain, missing_data_dict)
        return self.slack.generate_ok_message(domain)
