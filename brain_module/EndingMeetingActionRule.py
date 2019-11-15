import logging

from brain_module import Brain


class EndingMeetingActionRule:
    def __init__(self, brain: Brain, notify_minutes_to_end: int):
        self.brain = brain
        self.notify_minutes_to_end = notify_minutes_to_end
        self.events_notified_for_ending = {}

    def check_do(self):
        brain = self.brain
        for event in brain.current_open_events:
            if brain.calendar.is_event_ending(brain.current_time, event, self.notify_minutes_to_end):
                if event.id not in self.events_notified_for_ending:
                    logging.info(f'event {event.summary} is ending at {event.end}')
                    self.events_notified_for_ending[event.id] = True
                    time_in_minutes_until_end = brain.calendar.time_in_minutes_until_end(brain.current_time, event)
                    brain.speak.speak(f'This meeting reservation is ending in {time_in_minutes_until_end}. '
                                      f'Get the f out of here!')
                else:
                    logging.info(f'event {event.summary} is ending at {event.end} but message was already played.')
