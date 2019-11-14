from pytz import timezone


class CalendarConfig:
    calendar_timezone = timezone('Europe/Bucharest')
    event_close_message_template = 'Roompy was NOT happy the meeting room is kept reserved without anyone in it. ' \
                                   'Roompy has forcibly ended this meeting on {}.\n\n'
