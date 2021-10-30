from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence


@dataclass
class Instrument:
    id: int
    id_at_provider: str
    instrument_fields: List
    last_raw_data: Optional[Dict]


@dataclass
class DataProvider:
    id: int
    name: str
    description: str
    instruments: Sequence[Instrument]
