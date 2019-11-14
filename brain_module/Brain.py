import logging
from datetime import datetime

from calendar_module.Calendar import Calendar
from calendar_module.CalendarClient import CalendarClient
from speak_module.Speak import Speak


class Brain:
    def __init__(self):
        self.last_movement = datetime.fromisoformat('1000-01-01T00:00:00+02:00')
        self.calendar = Calendar(CalendarClient('adrian.tosca@gmail.com'))
        self.speak = Speak()
        self.events_notified_for_ending = {}

    def run_cycle(self):
        logging.info('running cycle')
        time_now = self.calendar.get_time_now()
        open_events = self.calendar.get_open_events(time_now)
        for event in open_events:
            if self.calendar.is_event_ending(time_now, event, 30):
                if event.id not in self.events_notified_for_ending:
                    logging.info(f'event {event.summary} is ending at {event.end}')
                    self.events_notified_for_ending[event.id] = True
                    time_in_minutes_until_end = self.calendar.time_in_minutes_until_end(time_now, event)
                    self.speak.speak(f'This meeting reservation is ending in {time_in_minutes_until_end}. '
                                     f'Get the f out of here!', 'en')
                else:
                    logging.info(f'event {event.summary} is ending at {event.end} but message already played.')

    def update_last_movement(self):
        print("last_movement updated")
        self.last_movement = datetime.now()
