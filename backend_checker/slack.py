from typing import Dict, List
from requests import post
from requests.exceptions import HTTPError, ConnectionError
from .dataclass import Instrument, DataProvider


class Slack:
    """Build messages and posts them on slack."""

    username = "SaaS Checker"

    def __init__(self, webhook_url: str):
        """Webhook Url."""
        self.webhook_url = webhook_url

    def send(self, payload: dict) -> None:
        """
        Send a json payload to a slack webhook.

        Params:
        - payload: Slack rich message payload

        Return:
        - None
        """
        post(url=self.webhook_url, json={"blocks": payload})

    @staticmethod
    def generate_divider():
        return {"type": "divider"}

    def generate_ok_message(self, domain: str):

        return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": (f"Report for domain: {domain}"),
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        ":ok_hand: All Connectors are up to date :ok_hand:"
                    ),
                },
            },
        ]

    def generate_error_message(self, domain: str, missing_data_dict: Dict):
        block = self.gen_header_error(domain)
        for provider in missing_data_dict.keys():
            missing_provider_data = missing_data_dict[provider]
            block += self.gen_dataprovider_block(
                provider, missing_provider_data
            )
            block.append(self.generate_divider())
        return block

    @staticmethod
    def gen_header_error(domain):
        return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": (f"Report for domain: {domain}"),
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        ":warning: Some Connectors "
                        "failed to fetch their daily data :warning: "
                    ),
                },
            },
        ]

    @staticmethod
    def gen_dataprovider_block(dataprovider_name: str, instruments: List):
        block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*DataProvider*: {dataprovider_name}",
                },
            }
        ]
        instruments = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*ID* {instrument.id} | *NAME* {instrument.id_at_provider} ",
                },
            }
            for instrument in instruments
        ]
        return block + instruments
