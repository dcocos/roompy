import logging
import unittest
from datetime import datetime, timedelta
from calendar_module.CalendarClient import CalendarClient
from calendar_module.test.TestConfig import TestConfig


class TestCalendarClient(unittest.TestCase):

    def setUp(self):
        self.test_date = datetime.fromisoformat('2019-11-14T00:00:00+02:00')
        self.calendar_client = CalendarClient(TestConfig.calendar_id)

    def test_list(self):
        result_list = self.list_on(self.test_date)
        logging.debug('Result list:')
        for e in result_list:
            logging.debug(e)
        self.assertEqual(len(result_list), 3)
        self.assertEqual(result_list[0].summary, 'Roompy Reservation Event TEST')

    def test_patch_end_time(self):
        result_list = self.list_on(self.test_date)
        first = result_list[0]
        self.calendar_client.patch_end_time(
            first,
            datetime.fromisoformat('2019-11-14T13:30:00+02:00')
        )
        result_list_after = self.list_on(self.test_date)
        first_after = result_list_after[0]
        self.assertEqual(first_after.end, datetime.fromisoformat('2019-11-14T13:30:00+02:00'))
        # put it back:
        self.calendar_client.patch_end_time(
            first_after,
            datetime.fromisoformat('2019-11-14T14:00:00+02:00')
        )

    def list_on(self, dt: datetime):
        return self.calendar_client.list(
            dt,
            dt + timedelta(hours=48)
        )


if __name__ == '__main__':
    unittest.main()
