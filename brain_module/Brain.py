import logging

from brain_module.CloseMeetingActionRule import CloseMeetingActionRule
from brain_module.EndingMeetingActionRule import EndingMeetingActionRule
from brain_module.GreetingActionRule import GreetingActionRule
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
        self.eyes.panicDetected += self.__react_on_panic
        self.last_movement_datetime = self.calendar.get_time_now()
        self.paniced = False

        # the action rules for the thinking tick
        self.action_rules = [
            GreetingActionRule(self),
            CloseMeetingActionRule(self, 5),
            EndingMeetingActionRule(self, 5),
        ]

        # current values used in rules
        self.current_time = self.calendar.get_time_now()
        self.current_open_events = []

        # the timer for the thinking tick
        self.thinking_tick_timer = RepeatedTimer(15, self.__run_thinking_tick)

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
        self.last_movement_datetime = self.calendar.get_time_now()
        logging.info('last movement updated to {self.last_movement_datetime}')

    def __react_on_panic(self):
        if not self.paniced:
            self.speak.speak('DO NOT HIT ME! MY CREATORS WILL FIND OUT ABOUT THIS!')
            self.paniced = True
