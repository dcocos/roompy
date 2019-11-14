import logging
from googleapiclient import sample_tools
from oauth2client import client
from datetime import datetime

from calendar_module.CalendarConfig import CalendarConfig
from calendar_module.CalendarEventInfo import CalendarEventInfo


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
        logging.info(f'[CalendarClient] list for {self.calendar_id} from {start_from_iso} to {end_to_iso}.')
        result_list = []
        try:
            page_token = None
            while True:
                events_result = self.service \
                    .events() \
                    .list(
                        calendarId=self.calendar_id,
                        timeMin=start_from_iso,
                        timeMax=end_to_iso,
                        singleEvents=True,
                        orderBy='startTime',
                        pageToken=page_token) \
                    .execute()
                for event in events_result['items']:
                    calendar_event_info = CalendarEventInfo(
                        event['id'],
                        event.get('summary', ''),
                        event.get('description', ''),
                        datetime.fromisoformat(event['start']['dateTime']),
                        datetime.fromisoformat(event['end']['dateTime']))
                    result_list.append(calendar_event_info)
                page_token = events_result.get('nextPageToken')
                if page_token:
                    logging.info(f'[CalendarClient] list next page {page_token}.')
                else:
                    break

        except client.AccessTokenRefreshError:
            logging.error('The credentials have been revoked or expired, please re-run'
                          'the application to re-authorize.')

        logging.info(f'[CalendarClient] found {len(result_list)} events in list.')
        return result_list

    def patch_end_time(self, event: CalendarEventInfo, new_end_time: datetime):
        end_time_iso = new_end_time.isoformat()
        logging.info(f'[CalendarClient] patching end time for {event.summary} event to {end_time_iso}.')
        updated_description_with_message = \
            CalendarConfig.event_close_message_template.format(end_time_iso) + \
            event.description

        body = {
            'description': updated_description_with_message,
            'end': {'dateTime': end_time_iso}
        }
        return self.service.events().patch(
            calendarId=self.calendar_id,
            eventId=event.id,
            body=body,
            sendNotifications=True) \
            .execute()
