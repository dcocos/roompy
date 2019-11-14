from dataclasses import dataclass
from datetime import datetime


@dataclass
class CalendarEventInfo:
    id: str
    summary: str
    description: str
    start: datetime
    end: datetime
