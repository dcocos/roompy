import logging
from datetime import timedelta

from brain_module import Brain


class CloseMeetingActionRule:
    def __init__(self, brain: Brain, no_move_minutes: int):
        self.brain = brain
        self.no_move_minutes = no_move_minutes

    def check_do(self):
        brain = self.brain
        if brain.last_movement_datetime + timedelta(minutes=self.no_move_minutes) < brain.current_time:
            logging.info(f'No movement in the last {self.no_move_minutes}, closing meeting event.')
            brain.calendar.close_all_open_events()
