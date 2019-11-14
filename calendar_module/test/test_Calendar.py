import unittest

from datetime import datetime
from unittest.mock import MagicMock

from calendar_module.CalendarClient import CalendarClient
from calendar_module.CalendarEventInfo import CalendarEventInfo
from calendar_module.Calendar import Calendar


class TestCalendar(unittest.TestCase):

    def setUp(self):
        self.time_now = datetime.fromisoformat('2019-11-14T10:00:00+02:00')
        self.calendar_client = CalendarClient('ci')
        self.calendar_event_list = [
            CalendarEventInfo('i1', 's1', 'd1',
                              datetime.fromisoformat('2019-11-14T03:00:00+02:00'),
                              datetime.fromisoformat('2019-11-14T04:00:00+02:00')),
            CalendarEventInfo('i1', 's1', 'd1',
                              datetime.fromisoformat('2019-11-14T08:00:00+02:00'),
                              datetime.fromisoformat('2019-11-14T09:00:00+02:00')),
            CalendarEventInfo('i1', 's1', 'd1',
                              datetime.fromisoformat('2019-11-14T09:30:00+02:00'),
                              datetime.fromisoformat('2019-11-14T10:30:00+02:00')),
            CalendarEventInfo('i1', 's1', 'd1',
                              datetime.fromisoformat('2019-11-14T11:00:00+02:00'),
                              datetime.fromisoformat('2019-11-14T12:00:00+02:00'))
        ]
        self.calendar_client.list = MagicMock(return_value=self.calendar_event_list)
        self.calendar_client.patch_end_time = MagicMock()

    def test_is_event_open_yes(self):
        calendar_manager = Calendar(self.calendar_client)
        time_now = datetime.fromisoformat('2019-11-14T08:30:00+02:00')
        test_event = CalendarEventInfo('ei', 'es', 'ed',
                                       datetime.fromisoformat('2019-11-14T08:00:00+02:00'),
                                       datetime.fromisoformat('2019-11-14T09:00:00+02:00'))
        self.assertTrue(calendar_manager.is_event_open(time_now, test_event))

    def test_is_event_open_no_less(self):
        calendar_manager = Calendar(self.calendar_client)
        time_now = datetime.fromisoformat('2019-11-14T07:50:00+02:00')
        test_event = CalendarEventInfo('ei', 'es', 'ed',
                                       datetime.fromisoformat('2019-11-14T08:00:00+02:00'),
                                       datetime.fromisoformat('2019-11-14T09:00:00+02:00'))
        self.assertFalse(calendar_manager.is_event_open(time_now, test_event))

    def test_is_event_open_no_more(self):
        calendar_manager = Calendar(self.calendar_client)
        time_now = datetime.fromisoformat('2019-11-14T09:10:00+02:00')
        test_event = CalendarEventInfo('ei', 'es', 'ed',
                                       datetime.fromisoformat('2019-11-14T08:00:00+02:00'),
                                       datetime.fromisoformat('2019-11-14T09:00:00+02:00'))
        self.assertFalse(calendar_manager.is_event_open(time_now, test_event))

    def test_list_around(self):
        calendar_manager = Calendar(self.calendar_client)
        result_list = calendar_manager.list_around(self.time_now, -4, 1)
        self.assertEqual(len(result_list), 4)

    def test_get_open_meetings(self):
        calendar_manager = Calendar(self.calendar_client)
        result_list = calendar_manager.get_open_events(self.time_now)
        self.assertEqual(len(result_list), 1)

    def test_close_all_open_meetings(self):
        calendar_manager = Calendar(self.calendar_client)
        calendar_manager.get_time_now = MagicMock(return_value=self.time_now)
        calendar_manager.close_all_open_events()
        self.calendar_client.patch_end_time.assert_called_once_with(self.calendar_event_list[2], self.time_now)

    def test_is_event_ending_no_before(self):
        calendar_manager = Calendar(self.calendar_client)
        time_now = datetime.fromisoformat('2019-11-14T08:30:00+02:00')
        test_event = CalendarEventInfo('ei', 'es', 'ed',
                                       datetime.fromisoformat('2019-11-14T08:00:00+02:00'),
                                       datetime.fromisoformat('2019-11-14T09:00:00+02:00'))
        self.assertFalse(calendar_manager.is_event_ending(time_now, test_event, 10))

    def test_is_event_ending_no_after(self):
        calendar_manager = Calendar(self.calendar_client)
        time_now = datetime.fromisoformat('2019-11-14T09:30:00+02:00')
        test_event = CalendarEventInfo('ei', 'es', 'ed',
                                       datetime.fromisoformat('2019-11-14T08:00:00+02:00'),
                                       datetime.fromisoformat('2019-11-14T09:00:00+02:00'))
        self.assertFalse(calendar_manager.is_event_ending(time_now, test_event, 10))

    def test_is_event_ending_yes(self):
        calendar_manager = Calendar(self.calendar_client)
        time_now = datetime.fromisoformat('2019-11-14T08:55:00+02:00')
        test_event = CalendarEventInfo('ei', 'es', 'ed',
                                       datetime.fromisoformat('2019-11-14T08:00:00+02:00'),
                                       datetime.fromisoformat('2019-11-14T09:00:00+02:00'))
        self.assertTrue(calendar_manager.is_event_ending(time_now, test_event, 10))


if __name__ == '__main__':
    unittest.main()
