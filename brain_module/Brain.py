import logging
from datetime import datetime

from calendar_module.Calendar import Calendar
from calendar_module.CalendarClient import CalendarClient


class Brain:
    def __init__(self):
        self.last_movement = datetime.fromisoformat('1000-01-01T00:00:00+02:00')
        self.calendar = Calendar(CalendarClient('adrian.tosca@gmail.com'))

    def run_cycle(self):
        logging.info('running cycle')
        open_events = self.calendar.get_open_events(self.calendar.get_time_now())
        for e in open_events:
            if self.calendar.is_event_ending(self.calendar.get_time_now(), e, 30):
                logging.info(f'event {e.summary} is ending at {e.end}')
