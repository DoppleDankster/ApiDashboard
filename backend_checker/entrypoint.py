from fire import Fire
from backend_checker.backend import BackendError, Backend
from backend_checker.slack import Slack
from backend_checker.display import Displayer
from backend_checker import Checker


def check(
    domain: str,
    username: str,
    password: str,
    display: bool = False,
    webhook_url: str = None,
):
    """
    Perform a check on the connectors of a backend.

    Args:
        :param domain(str): The base url of the backend ex: `api.datapred.com`
        :param username(str): The Login Username
        :param password(str): The Login Password
        :param display(bool): Flag to print informations on screen
        :param webhook_url(str): The slack webhook_url

    Returns:
        A web requests to Slack
    """
    backend = Backend(
        base_url=domain,
        username=username,
        password=password,
    )
    displayer = Displayer() if display else None
    slack = Slack(webhook_url=webhook_url) if webhook_url else None

    data_checker = Checker(backend, displayer, slack)
    data_checker.run()


def main():
    Fire(check)


if __name__ == "__main__":
    main()
