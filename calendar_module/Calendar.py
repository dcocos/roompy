import logging
from datetime import datetime, timedelta
from calendar_module.CalendarClient import CalendarClient
from calendar_module.CalendarEventInfo import CalendarEventInfo
from calendar_module.CalendarConfig import CalendarConfig


class Calendar:
    def __init__(self, calendar_client: CalendarClient):
        self.calendar_client = calendar_client

    def close_all_open_events(self):
        time_now = self.get_time_now()
        open_event_list = self.get_open_events(time_now)
        logging.info(f'[CalendarManager] Found {len(open_event_list)} open events.')
        for event in open_event_list:
            logging.info(f'[CalendarManager] Closing event {event.id} ({event.summary}).')
            self.calendar_client.patch_end_time(event, time_now)

    @staticmethod
    def get_time_now():
        return datetime.now(tz=CalendarConfig.calendar_timezone)

    @staticmethod
    def is_event_open(time_now: datetime, event_info: CalendarEventInfo):
        return event_info.start <= time_now <= event_info.end

    @staticmethod
    def is_event_ending(time_now: datetime, event_info: CalendarEventInfo, threshold_minutes: int):
        return event_info.end - timedelta(minutes=threshold_minutes) <= time_now <= event_info.end

    @staticmethod
    def time_in_minutes_until_end(time_now: datetime, event_info: CalendarEventInfo):
        if time_now < event_info.end:
            return (event_info.end - time_now).seconds / 60
        else:
            return -1

    def get_open_events(self, time_now: datetime):
        around_list = self.list_around(time_now, -4, 1)
        return [event for event in around_list if self.is_event_open(time_now, event)]

    def list_around(self, time_now: datetime, delta_hours_until: int, delta_hours_after: int):
        start_from = time_now + timedelta(hours=delta_hours_until)
        end_to = time_now + timedelta(hours=delta_hours_after)
        return self.calendar_client.list(start_from, end_to)
