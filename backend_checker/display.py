from typing import Sequence
from rich.console import Console
from rich.table import Table
from typing import Sequence
from .dataclass import DataProvider, Instrument


class Displayer:
    console = Console()

    def print_data_providers(self, providers: Sequence[DataProvider]):
        for provider in providers:
            if provider.instruments == []:
                continue
            table = self.generate_provider_table(provider)
            filled_table = self.fill_table(
                table=table, instruments=provider.instruments
            )
            self.console.print(table)

    def generate_provider_table(self, provider: DataProvider):
        table = Table(title=provider.name)
        table.add_column("Instrument Id")
        table.add_column("Instrument Name")
        table.add_column("Last Raw Data")
        return table

    def fill_table(self, table: Table, instruments: Sequence[Instrument]):
        for instrument in instruments:
            table.add_row(
                str(instrument.id),
                str(instrument.id_at_provider),
                str(instrument.last_raw_data),
            )
        return table
