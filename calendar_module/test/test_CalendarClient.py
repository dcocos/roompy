import unittest
from datetime import datetime, timedelta
from calendar_module.CalendarClient import CalendarClient


class TestCalendarClient(unittest.TestCase):

    def setUp(self):
        self.calendar_client = CalendarClient('adrian.tosca@gmail.com')

    def test_list(self):
        dt = datetime.fromisoformat('2019-11-14T00:00:00+02:00')
        start_from = dt
        end_to = dt + timedelta(hours=24)
        self.calendar_client.list(start_from, end_to)
