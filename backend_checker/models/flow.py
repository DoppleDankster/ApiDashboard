#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class Flow:
    id: int
    flow_name: str
    start_date: datetime
    start_date_updated_at: datetime
    run_frequency: str
    status: str
    loading_time_range: int
    retry_nb: int
    retry_counter: int
    modelling_group: int
    configuration: int
    decision_configuration: str
    price_drivers_config: int
