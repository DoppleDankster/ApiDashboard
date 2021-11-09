#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class Run:
    id: int
    integration_date: datetime
    production_date: datetime
    run_status: str
    flow: int
    complete: bool
