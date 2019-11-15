import logging
from datetime import datetime

from brain_module.CloseMeetingActionRule import CloseMeetingActionRule
from brain_module.EndingMeetingActionRule import EndingMeetingActionRule
from calendar_module.Calendar import Calendar
from calendar_module.CalendarClient import CalendarClient
from motion_module.Eyes import Eyes
from speak_module.Speak import Speak
from utils.RepeatedTimer import RepeatedTimer


class Brain:
    def __init__(self):
        # initialize the brain parts
        self.calendar = Calendar(CalendarClient('adrian.tosca@gmail.com'))
        self.speak = Speak()
        self.eyes = Eyes(True)
        self.eyes.motionDetected += self.__update_last_movement
        self.last_movement_datetime = datetime.fromisoformat('1000-01-01T00:00:00+02:00')

        # the action rules for the thinking tick
        self.action_rules = [
            EndingMeetingActionRule(self, 5),
            CloseMeetingActionRule(self, 5)
        ]

        # current values used in rules
        self.current_time = self.calendar.get_time_now()
        self.current_open_events = []

        # the timer for the thinking tick
        self.thinking_tick_timer = RepeatedTimer(5, self.__run_thinking_tick)

    def start_thinking(self):
        self.thinking_tick_timer.start()
        try:
            logging.info('Roompy is very vigilant')
            self.eyes.detect()
        finally:
            self.thinking_tick_timer.stop()
            logging.info('Roompy has fallen asleep')

    def __run_thinking_tick(self):
        logging.info('running thinking tick')
        self.current_time = self.calendar.get_time_now()
        self.current_open_events = self.calendar.get_open_events(self.current_time)
        for action_rule in self.action_rules:
            action_rule.check_do()

    def __update_last_movement(self):
        self.last_movement_datetime = datetime.now()
        logging.info(f'last movement updated to {self.last_movement_datetime}')
