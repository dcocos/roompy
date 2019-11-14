from googleapiclient import sample_tools
from oauth2client import client
from datetime import datetime


class CalendarClient:
    # http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html
    service, flags = sample_tools.init(
        [], 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar')

    def __init__(self, calendar_id: str):
        self.calendar_id = calendar_id

    def list(self, start_from: datetime, end_to: datetime):
        start_from_iso = datetime.isoformat(start_from)
        end_to_iso = datetime.isoformat(end_to)
        result_list = []
        try:
            page_token = None
            while True:
                print(start_from_iso + ' ' + end_to_iso)
                events_result = self.service \
                    .events() \
                    .list(
                        calendarId=self.calendar_id,
                        timeMin=start_from_iso,
                        timeMax=end_to_iso,
                        singleEvents=True,
                        pageToken=page_token) \
                    .execute()
                for event in events_result['items']:
                    print(event)
                page_token = events_result.get('nextPageToken')
                if not page_token:
                    break

        except client.AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-run'
                  'the application to re-authorize.')

        return result_list
